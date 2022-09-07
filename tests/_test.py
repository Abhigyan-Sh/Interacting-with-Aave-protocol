from brownie import accounts, network, config, interface

LOCAL_DEVELOPMENT_NETWORKS= ['development', 'mainnet-fork', 'mainnet-fork-dev']

def get_account(id= None, index= None):
    if id:
        return accounts.load(id)
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_DEVELOPMENT_NETWORKS:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])

def ethToWeth(amount):
    weth_contract= interface.IWETH(config['networks'][network.show_active()]['weth'])
    # txn= weth_contract.deposit({'from': get_account(), 'value': amount})
    # txn.wait(1)
    assert weth_contract.address== config['networks'][network.show_active()]['weth']