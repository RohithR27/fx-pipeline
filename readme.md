# FX Rates Pipeline

A small ETL pipeline in Python and SQL that cleans foreign exchange rate data.

## What it does
- **Extract:** reads rates from CSV data
- **Transform:** trims and uppercases currency codes, converts rates to numbers, rejects bad rows
- **Load:** stores clean rows in a SQLite table
- Reports how many rows were read, cleaned and rejected

## How to run
python pipeline.py

## What I learned
Learned about the SQL and python basics and did one basic ETL flow and psuhed the code though git cmds