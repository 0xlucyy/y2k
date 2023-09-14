
'''

  Params:
  - _NAME (str): labelName of a domain, ie .. without .eth part.
'''
GET_Y2K_MARKETS = '''
{
  markets(
    where:{

    }
    block:{
      number_gte:33934301
    }
    orderBy:tvl
    orderDirection:desc
  )
  {
    id
    isV2
    premiumVault
    collateralVault
    strikePrice
    depositAsset
    formattedStrikePrice
    token
    marketName
    marketIndex
    controller
    tvl
    activeUsers
    protocolFees
    collateralFees
    premiumFees
    collateralTVL
    premiumTVL
    paused
  }
}
'''


'''


  Params:
  - _SKIP (int): increments of 100
'''
GET_Y2K_USER = '''
{
users(
  where:{
    id:"0x0aae9ae032b04fb8ac1f6265ecd7710f443995c6"
  }
  block:{
    number_gte:33934301
  }
  skip:_SKIP
)
  {
    id
		emissions
    __typename
    depositAssets{
      depositAsset
      collateralTVL
      collateralProfit
      premiumTVL
      premiumProfit
      tvl
      tvlV2
      tvlV1
      pnl
      id
    }
  }
}
'''

GET_Y2K_USER = '''
{
users(
  where:{id:"0x0aae9ae032b04fb8ac1f6265ecd7710f443995c6"}
  block:{
    number_gte:33934301
  }
)
  {
    id
		emissions
    __typename
    depositAssets{
      depositAsset
      collateralTVL
      collateralProfit
      premiumTVL
      premiumProfit
      tvl
      tvlV2
      tvlV1
      pnl
      id
    }
  }
}
'''