# Task Planner Pro

**Task Planner Pro** este o aplicație de gestionare a sarcinilor (to-do list) construită în Python folosind Tkinter pentru interfața grafică și SQLite pentru stocarea datelor. Aplicația permite adăugarea, modificarea și ștergerea sarcinilor, precum și filtrarea acestora pe baza priorității și stării (în curs, finalizată).

## Funcționalități

- Adăugarea de sarcini cu titlu, categorie, subcategorie, dată limită, prioritate și stare.
- Afișarea sarcinilor în ordine cronologică în secțiunea Dashboard.
- Filtrarea și căutarea sarcinilor după categorie și stare.
- Statistici grafice pentru sarcinile finalizate vs. sarcinile în curs.
- Setări pentru schimbarea temei aplicației (light, dark, colorful).
- Export sarcini în formate CSV, PDF, Excel, și JSON.

## Tehnologii utilizate

- **Python** - limbaj de programare principal
- **Tkinter** - pentru crearea interfeței grafice
- **SQLite** - pentru gestionarea bazei de date a sarcinilor
- **Matplotlib** - pentru generarea graficelor
- **Tkcalendar** - pentru selecția ușoară a datelor

## Cerințe de sistem

- Python 3.x instalat
- Biblioteca `Tkinter` (inclusă cu majoritatea distribuțiilor de Python)
- Dependențe suplimentare specificate în secțiunea de instalare

## Instalare

### 1. Clonează proiectul de pe GitHub

Pentru a clona acest proiect, rulează comanda următoare într-un terminal:

```bash
git clone https://github.com/numele-tau/task_planner_pro.git
cd task_planner_pro
