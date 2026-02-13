#!/bin/bash

for f in *.jpg *.JPG *.jpeg *.JPEG; do
  # Salta se il pattern non matcha nessun file
  [ -e "$f" ] || continue
  
  # Estrae data in formato YYYY-MM-DD (primi 10 caratteri)
  date_str=$(mdls --raw -name kMDItemContentCreationDate "$f" | cut -c 1-10)
  # Estrae ora in formato HH-mm-ss (caratteri successivi)
  time_str=$(mdls --raw -name kMDItemContentCreationDate "$f" | cut -c 12-19)

  # Se mdls non restituisce una data valida, skippa
  if [[ ! "$date_str" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "Skipping $f (no valid date: $date_str)"
    continue
  fi
  
  # Rimuove i trattini: YYYY-MM-DD → YYYYMMDD
  date_compact="${date_str//-/}"
  # Rimuove i due punti: HH:mm:ss → HHmmss
  time_str="${time_str//:/}"
  
  # Separa nome ed estensione
  base="${f%.*}"
  ext="${f##*.}"
  
  # Costruisce il nuovo nome
  new_name="${base}_${date_compact}_${time_str}.${ext}"
  
  # Rinomina (-n per evitare sovrascrittura)
  mv -n "$f" "$new_name"
  echo "Renamed: $f → $new_name"
done
