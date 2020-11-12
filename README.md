# kgtk-delta-wikidata
This repository contains the code for calculating  deltas from two sorted kgtk files. The effort is targeted towards capturing the differences between different Wikidata endpoints


To use the script just type:

```
python calculate_deltas.py -o path_to_old_dataset -n path_to_new_dataset -d output_directory
```

Where `path_to_old_dataset` is the path to the oldest dataset taking part in the comparison; `path_to_new_dataset` is the most recent dataset, and `output_directory` is the directory where the outputs will be written to. Three outputs will be produced: `added.tsv`, which contains the statements that have been newly added in the more recent dataset; `deleted.tsv` wich contains the statements that have been deleted in the most recent dataset; and `modified_qual.tsv`, which contains those statements which have qualifiers that have been modified.

For all files, only id, node1, label, node2 is kept for simplicity.