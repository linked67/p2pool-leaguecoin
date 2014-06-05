import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

@defer.inlineCallbacks
def get_subsidy(bitcoind, target):
    res = yield bitcoind.rpc_getblock(target)

    defer.returnValue(res)

nets = dict(

  leaguecoin=math.Object(
        P2P_PREFIX='a1a0a2a3'.decode('hex'),
        P2P_PORT=19667,
        ADDRESS_VERSION=48,
        RPC_PORT=19668,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'LeagueCoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        #SUBSIDY_FUNC=lambda nBits, height: __import__('hackcoin_subsidy').GetBlockBaseValue(nBits, height),
        SUBSIDY_FUNC=lambda bitcoind, target: get_subsidy(bitcoind, target),
        BLOCK_PERIOD=60, # s
        SYMBOL='LOL',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'LeagueCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/LeagueCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.LeagueCoin'), 'LeagueCoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='',
        ADDRESS_EXPLORER_URL_PREFIX='',
        TX_EXPLORER_URL_PREFIX='',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),




)
for net_name, net in nets.iteritems():
    net.NAME = net_name
