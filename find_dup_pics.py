#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from PIL import Image
import imagehash
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.panel import Panel
import questionary

console = Console()
THRESHOLD = 5

def pick_folder(start_path="."):
    """Navigatore interattivo per scegliere la cartella"""
    current_path = Path(start_path).resolve()
    
    while True:
        # Elenca cartelle nella directory corrente
        try:
            items = [p for p in current_path.iterdir() if p.is_dir() and not p.name.startswith('.')]
            items.sort(key=lambda p: p.name.lower())
        except PermissionError:
            console.print(f"[red]🚫 Access denied: {current_path}[/red]")
            current_path = current_path.parent
            continue

        # Opzioni per il menu
        choices = [
            questionary.Choice(title=f"📂 {current_path.name} (SELECT THIS)", value="SELECT"),
            questionary.Choice(title="⬆️  .. (Go Up)", value="UP"),
        ] + [
            questionary.Choice(title=f"📁 {p.name}", value=p) for p in items
        ]

        selection = questionary.select(
            f"Navigate: {current_path}",
            choices=choices,
            use_indicator=True,
            style=questionary.Style([
                ('qmark', 'fg:#673ab7 bold'),       # Colore simbolo domanda
                ('question', 'bold'),               # Colore domanda
                ('answer', 'fg:#f44336 bold'),      # Colore risposta
                ('pointer', 'fg:#673ab7 bold'),     # Colore puntatore
                ('highlighted', 'fg:#673ab7 bold'), # Colore selezione
                ('selected', 'fg:#cc5454'),         # Colore item selezionato
                ('separator', 'fg:#cc5454'),
                ('instruction', ''),
                ('text', ''),
                ('disabled', 'fg:#858585 italic')
            ])
        ).ask()

        if selection == "SELECT":
            return current_path
        elif selection == "UP":
            current_path = current_path.parent
        elif selection is None: # Utente preme Ctrl+C
            sys.exit(0)
        else:
            current_path = selection

def main():
    console.print(Panel.fit("[bold cyan]🔍 Image Duplicate Finder[/bold cyan]", border_style="cyan"))

    # 1. Selezione Cartella Interattiva
    image_dir = pick_folder()
    
    console.print(f"\n[bold green]📂 Selected:[/bold green] {image_dir}\n")

    # 2. Raccolta File
    extensions = {"*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG"}
    image_files = []
    for ext in extensions:
        image_files.extend(image_dir.glob(ext))
    
    image_files = sorted(list(set(image_files))) 
    
    if not image_files:
        console.print("[yellow]⚠️  Nessuna immagine trovata nella cartella.[/yellow]")
        return

    # 3. Calcolo Hash
    hashes = {}
    errors = []

    for img_path in track(image_files, description="[cyan]Processing images...[/cyan]"):
        try:
            with Image.open(img_path) as img:
                hashes[img_path.name] = imagehash.phash(img)
        except Exception as e:
            errors.append((img_path.name, str(e)))

    if errors:
        console.print(f"\n[bold red]Errors ({len(errors)}):[/bold red]")
        for name, err in errors:
            console.print(f"  ❌ {name}: {err}")

    # 4. Confronto
    duplicates = []
    seen = set()
    items = list(hashes.items())
    total_comparisons = (len(items) * (len(items) - 1)) // 2
    
    with console.status(f"[bold green]Comparing {total_comparisons} pairs...[/bold green]"):
        for i, (name1, hash1) in enumerate(items):
            for name2, hash2 in items[i+1:]:
                hamming_dist = hash1 - hash2
                if hamming_dist <= THRESHOLD:
                    pair = tuple(sorted([name1, name2]))
                    if pair not in seen:
                        duplicates.append((name1, name2, hamming_dist))
                        seen.add(pair)

    # 5. Tabella Risultati
    if duplicates:
        console.print(f"\n[bold green]✅ Found {len(duplicates)} duplicate pair(s):[/bold green]")
        
        table = Table(title="Duplicate Candidates", show_header=True, header_style="bold magenta")
        table.add_column("File A", style="cyan")
        table.add_column("File B", style="cyan")
        table.add_column("Dist", justify="center", style="yellow")
        
        for f1, f2, dist in duplicates:
            dist_str = f"[bold green]{dist}[/bold green]" if dist == 0 else str(dist)
            table.add_row(f1, f2, dist_str)
            
        console.print(table)
    else:
        console.print("\n[bold green]✨ No duplicates found. Clean![/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
