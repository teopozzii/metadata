#!/usr/bin/env python3
import os
from pathlib import Path
from PIL import Image
import imagehash
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

# Configurazione
THRESHOLD = 5

def main():
    console.print(Panel.fit("[bold cyan]🔍 Image Duplicate Finder[/bold cyan]", border_style="cyan"))

    # 1. Input Cartella
    path_input = Prompt.ask("Inserisci il percorso della cartella", default=".")
    image_dir = Path(path_input)

    if not image_dir.exists():
        console.print(f"[bold red]❌ Errore:[/bold red] La cartella '{image_dir}' non esiste.")
        return

    # 2. Raccolta File
    extensions = {"*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG"}
    image_files = []
    for ext in extensions:
        image_files.extend(image_dir.glob(ext))
    
    image_files = sorted(list(set(image_files))) # Rimuove duplicati e ordina
    
    if not image_files:
        console.print("[yellow]⚠️  Nessuna immagine trovata nella cartella.[/yellow]")
        return

    console.print(f"[green]Found {len(image_files)} images.[/green] Calculating hashes...")

    # 3. Calcolo Hash con Progress Bar
    hashes = {}
    errors = []

    for img_path in track(image_files, description="Processing..."):
        try:
            with Image.open(img_path) as img:
                hashes[img_path.name] = imagehash.phash(img)
        except Exception as e:
            errors.append((img_path.name, str(e)))

    # Stampa errori se ci sono
    if errors:
        console.print(f"\n[bold red]Errors ({len(errors)}):[/bold red]")
        for name, err in errors:
            console.print(f"  ❌ {name}: {err}")

    # 4. Confronto (O(n^2))
    duplicates = []
    seen = set()
    items = list(hashes.items())

    # Usiamo una progress bar anche per il confronto se ci sono molti file
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
            # Colora la distanza: verde = identico, giallo = simile
            dist_str = f"[bold green]{dist}[/bold green]" if dist == 0 else str(dist)
            table.add_row(f1, f2, dist_str)
            
        console.print(table)
    else:
        console.print("\n[bold green]✨ No duplicates found. Clean![/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]🚫 Interrotto dall'utente.[/bold red]")
