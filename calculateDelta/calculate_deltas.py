# License to be applied

# This script will load 2 KGTK files passed as input parameters and write out three different files:
# A file with the added statements.
# A file with the deleted statements
# A file with the modified statements.

import sys, getopt
import csv
import os


# Assumption: both files are sorted.
# Assumption: both files have an id field.
# Assumption: ids look like Q3534556-P7598-1 (3 parts: QNode, PNode and hash of qualifiers)
def calculate_deltas(old_file, new_file, output_dir):
    """
    Function that takes 2 wikidata files and calculates a delta between them.
    3 files are generated:
    * added.tsv contains the statements from new_file that are not in old_file
    * deleted.tsv contains the statements in old_file which are not in new_file
    * modified_qual.tsv contains the statements which have been modified in qualifiers, i.e., that have same
    subject, predicate, object but different id in their qualifiers.
    Statements that are modified in the value will appear as deleted/added.
    """
    print('Calculating deltas for files: \n OLD: ' + old_file + "\n NEW: " + new_file)
    print('Output will be written to directory: ' + output_dir)
    output_added = os.path.join(output_dir, "added.tsv")
    output_deleted = os.path.join(output_dir, "deleted.tsv")
    output_modified = os.path.join(output_dir, "modified_qual.tsv")
    with open(output_added, "w",encoding="utf-8", newline='') as added_file:
        added_tsv = csv.writer(added_file, delimiter='\t')
        added_tsv.writerow(['id', 'node1', 'label', 'node2'])
        with open(output_deleted, "w",encoding="utf-8", newline='') as deleted_file:
            deleted_tsv = csv.writer(deleted_file, delimiter='\t')
            deleted_tsv.writerow(['id', 'node1', 'label', 'node2'])
            with open(output_modified, "w",encoding="utf-8", newline='') as modified_file:
                modified_tsv = csv.writer(modified_file, delimiter='\t')
                modified_tsv.writerow(['id', 'node1', 'label', 'node2'])
                with open(old_file, encoding="utf-8") as old_kgtk_file:
                    old_kgtk = csv.reader(old_kgtk_file, delimiter="\t")
                    with open(new_file, encoding="utf-8") as new_kgtk_file:
                        new_kgtk = csv.reader(new_kgtk_file, delimiter="\t")
                        line_new = next(new_kgtk)
                        line_old = next(old_kgtk)
                        # Extract position of headers (label, node1, etc) as they could be different in the files
                        p_new = extract_positions(line_new)
                        p_old = extract_positions(line_old)
                        print('ID position in OLD file: ' + str(p_old['id']) + ", ID position in NEW file: " + str(
                            p_new['id']))
                        line_new = next(new_kgtk)
                        id_new = line_new[p_new['id']]
                        for line_old in old_kgtk:
                            id_old = line_old[p_old['id']]
                            while id_old > id_new :
                                # Have we finished parsing new_file? then all old statements have been deleted
                                if line_new is None:
                                    # print('Deleted statement: ' + id_old)
                                    write_statement_to_file(deleted_tsv, line_old, p_old)
                                    break
                                # If node1, node2 and label are the same but the id is not, then it has been modified.
                                elif ((line_new[p_new['node1']] == line_old[p_old['node1']]) and
                                    (line_new[p_new['node2']] == line_old[p_old['node2']]) and
                                    (line_new[p_new['label']] == line_old[p_old['label']])):
                                    write_statement_to_file(modified_tsv, line_new, p_new)
                                    # print('Modified statement: ' + id_new)
                                    break
                                    # break because we need to increase id_old
                                else:
                                    # print('Added statement: ' + id_new)
                                    write_statement_to_file(added_tsv, line_new, p_new)
                                line_new = next(new_kgtk, None)
                                if line_new is not None:
                                    id_new = line_new[p_new['id']]
                            if id_old < id_new:
                                if (line_new is not None and (line_new[p_new['node1']] == line_old[p_old['node1']]) and
                                    (line_new[p_new['node2']] == line_old[p_old['node2']]) and
                                    (line_new[p_new['label']] == line_old[p_old['label']])):
                                    write_statement_to_file(modified_tsv, line_new, p_new)
                                    # print('Modified statement: ' + id_new)
                                    line_new = next(new_kgtk, None)
                                    if line_new is not None:
                                        id_new = line_new[p_new['id']]
                                else:
                                    # print('Deleted statement: ' + id_old)
                                    write_statement_to_file(deleted_tsv, line_old, p_old)
                            else:
                                # if both are the same, then continue
                                line_new = next(new_kgtk, None)
                                if line_new is not None:
                                    id_new = line_new[p_new['id']]
                        # The remaining statements (if any) belong to the added file
                        while line_new is not None:
                            # print('Added statement1: ' + id_new)
                            write_statement_to_file(added_tsv, line_new, p_new)
                            line_new = next(new_kgtk, None)
                            if line_new is not None:
                                id_new = line_new[p_new['id']]

    pass


def extract_positions(line):
    """This method returns the position of each header in a KGTK file"""
    positions = {'id': line.index('id'), 'node1': line.index('node1'), 'node2': line.index('node2'),
                 'label': line.index('label')}
    return positions


def write_statement_to_file(file_writer, statement, positions):
    """This method writes a statement into a KGTK file following the headers in positions"""
    file_writer.writerow([statement[positions['id']], statement[positions['node1']],
                          statement[positions['label']], statement[positions['node2']]])


def main(argv):
    old_file = ''
    new_file = ''
    output_dir = ''
    try:
        opts, args = getopt.getopt(argv, "ho:n:d:", ["old_file=", "new_file=", "dir="])
        # print("OPTS: " + str(opts))
        # print("ARGS" + str(args))
    except getopt.GetoptError:
        print('calculate_deltas.py -o <old_file> -n <new_file> -d <directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--h':
            print('calculate_deltas.py -o <old_file> -n <new_file> -d <directory>')
            sys.exit()
        elif opt in ("-o", "--old_file"):
            old_file = arg
        elif opt in ("-n", "--new_file"):
            new_file = arg
        elif opt in ("-d", "--dir"):
            output_dir = arg

    # If files are not empty, proceed.
    if old_file and new_file:
        calculate_deltas(old_file, new_file, output_dir)
    else:
        print('Input files cannot be empty')
        print('calculate_deltas.py -o <old_file> -n <new_file> -d <directory>')


if __name__ == "__main__":
    main(sys.argv[1:])
