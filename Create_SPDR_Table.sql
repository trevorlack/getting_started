CREATE TABLE `spdr_holdings` (
  `Holdings_Date` date NOT NULL,
  `ISIN` varchar(15) NOT NULL,
  `FUND_ID` varchar(5) NOT NULL,
  `Asset_Class` varchar(6) NOT NULL,
  `Weight` decimal(8,6) DEFAULT NULL,
  `Market_Value` decimal(22,6) DEFAULT NULL,
  `Coupon` decimal(10,4) DEFAULT NULL,
  `Maturity` date DEFAULT NULL,
  `Cusip` varchar(10) NOT NULL,
  PRIMARY KEY (`Holdings_Date`,`ISIN`,`FUND_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='\nBloomberg Formula to capture historic bid pricing for the bonds\n=BDH(B10&"@BVAL Corp","BID","12/27/17 15:00","12/27/17 15:00","IntrRw=True","cols=4;rows=1")';
