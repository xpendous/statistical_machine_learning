
import random

TRAIN_SET = "data/train.txt"
PAIR_SET_WHOLE = "data/pair_set_whole.txt"

PAIR_SET_PROPORTION = "data/pair_set_proportion.txt"
PAIR_SET_TRAIN = "data/pair_set_train.txt"
PAIR_SET_TEST = "data/pair_set_test.txt"


# TODO: change ratio to 0.8 and 0.2 for final
# small pair set is 0.001 of entire train set
proportion = 0.1
# train set from small pair set
train_ratio = 1.0
# valid set from same pair set
test_ratio = 0.0001

# generate complete pair set from training set
def generateWholePairSet():
    f_train = open(TRAIN_SET)
    f_whole_pair_set = open(PAIR_SET_WHOLE, "w")

    line_num = 0
    for line in f_train:
        line_num += 1
        line = line.strip("\n").split("\t")
        item_num = 0
        src = line[0]
        for item in line:
            item_num += 1
            if item_num > 1:
                print >> f_whole_pair_set, "\t".join([src, item])

    f_train.close()
    f_whole_pair_set.close()


def generateProportionPairSet():
    f_whole_pair_set = open(PAIR_SET_WHOLE)
    f_pair_set_proportion = open(PAIR_SET_PROPORTION, "w")

    lines = [line.strip("\n") for line in f_whole_pair_set]
    random_lines = random.sample(lines, int(len(lines) * proportion))
    f_pair_set_proportion.write("\n".join(random_lines))

    f_whole_pair_set.close()
    f_pair_set_proportion.close()


# mock and split training set and validatio set
# small train set is 0.0001 of entire train set
# small valid set is 0.2 of entire train set
def generateTrainTestPairSet():
    f_pair_set_proportion = open(PAIR_SET_PROPORTION)
    f_pair_set_train = open(PAIR_SET_TRAIN, "w")
    f_pair_set_test = open(PAIR_SET_TEST, "w")

    lines = [line.strip("\n") for line in f_pair_set_proportion]

    # get training pair set
    random_lines = random.sample(lines, int(len(lines) * train_ratio))
    f_pair_set_train.write("\n".join(random_lines))

    # get test pair set
    random_lines = random.sample(lines, int(len(lines) * test_ratio))
    f_pair_set_test.write("\t".join(["ID", "from", "to"]) + "\n")
    line_num = 0
    for random_line in random_lines:
        line_num += 1
        f_pair_set_test.write(str(line_num) + "\t")
        f_pair_set_test.write(random_line + "\n")



    f_pair_set_proportion.close()
    f_pair_set_train.close()
    f_pair_set_test.close()


if __name__ == '__main__':
    generateWholePairSet()
    generateProportionPairSet()
    generateTrainTestPairSet()

