import argparse
import logging

import chainer

from listnet import dataset, training
from listnet.model import ListNet

logging.basicConfig(level=logging.INFO)

def run(args):
    logging.info("Loading dataset")

    train = dataset.create_dataset(args.train)
    logging.info("loaded {} sets for training".format(len(train)))

    dev = dataset.create_dataset(args.dev)
    logging.info("loaded {} sets for dev".format(len(dev)))

    test = dataset.create_dataset(args.test)
    logging.info("loaded {} sets for test".format(len(test)))

    listnet = ListNet(train[0][0].shape[1], 200, 0.0)
    optimizer = chainer.optimizers.Adam(alpha=0.0007)
    optimizer.setup(listnet)
    optimizer.add_hook(chainer.optimizer.WeightDecay(0.0005))
    #optimizer.add_hook(chainer.optimizer.GradientClipping(5.))

    train_itr = chainer.iterators.SerialIterator(train, batch_size=1)
    training.train(listnet, optimizer, train_itr, 1000, dev=dev,
                   device=None)
    loss, acc = training.forward_pred(listnet, test, device=None)
    logging.info("Test => loss={:0.6f} acc={:0.6f}".format(loss, acc))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--train', required=True, type=str,
                   help='SNLI train json file path')
    p.add_argument('--dev', required=True, type=str,
                   help='SNLI dev json file path')
    p.add_argument('--test', required=True, type=str,
                   help='SNLI test json file path')

    # optional
    p.add_argument('-g', '--gpu', type=int, default=None, help="GPU number")
    args = p.parse_args(["--train", "MQ2008/Fold1/train.txt",
                         "--dev", "MQ2008/Fold1/vali.txt",
                         "--test", "MQ2008/Fold1/test.txt"])

    run(args)
