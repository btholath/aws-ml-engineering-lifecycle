#!/usr/bin/python3

import sys
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


if len(sys.argv) != 2:
  print("Usage: {} <path_to_csv>".format(sys.argv[0]))
  sys.exit()

csv_file = sys.argv[1]
parquet_file = sys.argv[1].replace("csv", "parquet")
print("Input file: {}".format(csv_file))
print("Output file: {}".format(parquet_file))

chunksize = 100_000

csv_stream = pd.read_csv(csv_file, sep=',', chunksize=chunksize, low_memory=False)

for i, chunk in enumerate(csv_stream):
    if i == 0:
        # Guess the schema of the CSV file from the first chunk
        parquet_schema = pa.Table.from_pandas(df=chunk).schema
        print("Derived Schema:")
        print(parquet_schema)
        # Open a Parquet file for writing
        parquet_writer = pq.ParquetWriter(parquet_file, parquet_schema, compression='snappy')
    # Write CSV chunk to the parquet file
    table = pa.Table.from_pandas(chunk, schema=parquet_schema)
    parquet_writer.write_table(table)

parquet_writer.close()
