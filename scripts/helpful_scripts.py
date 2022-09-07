from web3 import Web3
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
    txn= weth_contract.deposit({'from': get_account(), 'value': amount}) # hence deposit is a payable function
    txn.wait(1)
    return weth_contract.address
# we suppose that 
# config['networks'][network.show_active()]['weth']
# and
# weth_contract.address ,these addresses are same here need to confirm 
# once i get enough kovan token i will confirm this

def getLendingPool():
    ILendingPoolAddressProvider= interface.ILendingPoolAddressesProvider(config['networks'][network.show_active()]['ILendingPoolAd_Prov_address'])
    LendingPool_address= ILendingPoolAddressProvider.getLendingPool()
    LendingPool= interface.ILendingPool(LendingPool_address)
    return LendingPool

def approving(asset, spender, amount):
    ierc20= interface.IERC20(asset)
    txn= ierc20.approve(spender, amount,{"from":get_account()})
    txn.wait(1)

def userAccountData():
    LendingPool= getLendingPool()
    (totalCollateralETh,
    totalDebtETH,
    availableBorrowsETH,
    currentLiquidationThreshold,
    ltv,
    healthFactor)= LendingPool.getUserAccountData()
    totalCollateralETh= Web3.fromWei(totalCollateralETh, "ether")
    totalDebtETH= Web3.fromWei(totalDebtETH, "ether")
    availableBorrowsETHs= availableBorrowsETH
    availableBorrowsETH= Web3.fromWei(availableBorrowsETH, "ether")
    print(f'Total Collateral Eth is: {totalCollateralETh}')
    print(f'Total debt eth is {totalDebtETH}')
    print(f'Total amount which can be borrowed is {availableBorrowsETH}')
    print(f'Liquidation threshold is {currentLiquidationThreshold}')
    print(f'loan to value is {ltv}')
    print(f'health factor is {healthFactor}')
    return availableBorrowsETHs

def borrower(Dai_address, Borrowable_amount, interestRateMode, referralCode, onBehalfOf):
    LendingPool= getLendingPool()
    txn= LendingPool.borrow(Dai_address, Borrowable_amount, interestRateMode, referralCode, onBehalfOf, {"from":get_account()})
    txn.wait(1)
