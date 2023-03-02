'''
  Returns 

  Params:
  - 
'''
BOND_TOKENS = '''
{
  bondTokens(
    where: {
      symbol_starts_with: "Y2K"}, 
    orderBy: expiry,
    orderDirection: desc,
    block: {
      number_gte: 9380410
    }
  ) 
  {
    id
    decimals
    network
    chainId
    symbol
    expiry
    teller
    type
    underlying{
      id
      network
      chainId
      address
      symbol
      name
      typeName
    }
  }
}
'''


'''
  Returns 

  Params:
  - 
'''
MARKETS = '''
{
  markets(
    where: {
      payoutToken_: {
        name: "Y2K",
        symbol_not: "Dummy"
      },
      isLive: true
    }
  )
  {
    id
    name
    network
    chainId
    auctioneer
    teller
    marketId
    owner
    vesting
    vestingType
    creationBlockTimestamp
    capacity
    quoteToken {
      id
      symbol
      name
    }
    payoutToken{
      id
      symbol
      name
    }
  }
}
'''


'''
  Returns 

  Params:
  - 
'''
ownerTokenTbvs = '''
{
	ownerTokenTbvs(
    where: {
      owner:"0x5c84cf4d91dc0acde638363ec804792bb2108258"
    }
  )
  {
    id
    owner
    token
    network
    tbv
  }
}
'''


BOND_PURCHASES = '''
{
	bondPurchases(
    where: {
      payoutToken_: {
        name: "Y2K",
        symbol_not: "Dummy"
      }
    },
    orderBy: timestamp,
    orderDirection: desc
    
  ) {
    id
    marketId
    owner
    amount
    payout
    recipient
    referrer
    timestamp
    teller
    network
    chainId
    purchasePrice
    postPurchasePrice
    ownerTokenTbv {
      id
      owner
      token
      network
      chainId
      tbv
    }
    quoteToken {
      id
      symbol
      name
    }
    payoutToken{
      id
      symbol
      name
    }
  }
}
'''