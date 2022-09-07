from scripts.helpful_scripts import (
    ethToWeth, 
    getLendingPool, 
    get_account, 
    approving,
    userAccountData,
    borrower)
from web3 import Web3
from brownie import config, network, interface

def deploy():
# @dev::: depositing to WETH contract
    amount= Web3.toWei(0.1, 'ether')
    wethContract_address= ethToWeth(amount)
# @dev::: approve to spender address by asset address
    LendingPool= getLendingPool()
    approving(wethContract_address, LendingPool.address, amount)
# @dev::: deposit WETH to Aave
    LendingPool.deposit(wethContract_address, amount, get_account(), 0, {"from":get_account()})
# @dev::: Get to see the status
    # commented since if we look at next method which has been called borrowerTaker,
    # so we realize that it calls this method in which currentstatus gets printed on terminal..
    # userAccountData()
# @dev::: borrow WETH from Aave
    Dai_address= config['networks'][network.show_active()]['DaiToken']
    Borrowable_amount= borrowerTaker(Dai_address)
# @dev::: Get to see the status
    userAccountData()
# @dev::: approve to spender address by asset address
    approving(Dai_address, LendingPool.address, Borrowable_amount)
    LendingPool.repay(Dai_address, Borrowable_amount, 1, get_account(), {"from":get_account()})
# @dev::: Get to see the status
    userAccountData()

def borrowerTaker(Dai_address):
    # @dev::: eth to be converted to Dai so as i can ask for that much
    _priceFeed= config['networks'][network.show_active()]['DaiToeth_priceFeed']
    AggregatorV3Interface= interface.AggregatorV3Interface(_priceFeed)
    price_DaiToEth= AggregatorV3Interface.latestRoundData()[1]
    adjusted_price= price_DaiToEth*10**10
    Borrowable_amount= userAccountData()
    Borrowable_amount= (Borrowable_amount *10**18/ adjusted_price)
    
    borrower(Dai_address, Borrowable_amount, 1, 0, get_account())
    return Borrowable_amount
