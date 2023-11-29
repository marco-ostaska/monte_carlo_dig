item = {'Titulo': 'Maior sortino ratio', 'Retorno': 25.38040429210423, 'Risco': 6.9357963750233145, 'RiscoAjustado': 3.6436626012605418, 'Sharpe': 2.556361711533757, 'Sortino': 4.866093882010457, 'Tickers': {'HSML11.SA': 0.20653908897174264, 'GALG11.SA': 2.074572131668715, 'IFRA11.SA': 3.519745573861862, 'XPML11.SA': 1.1116309151941277, 'HGBS11.SA': 4.000231113047354, 'RURA11.SA': 2.800815605016329, 'MAXR11.SA': 4.336996157840831, 'BCRI11.SA': 4.551841094966636, 'BTAL11.SA': 4.1611366031034045, 'AGRO3.SA': 1.4468416725023374, 'TAEE11.SA': 0.9669955228642703, 'SAPR3.SA': 0.9141394308952158, 'JALL3.SA': 0.7622661006252877, 'CMIG4.SA': 3.4643507158837625, 'HSAF11.SA': 1.5300451854208161, 'XPIN11.SA': 4.001471682504139,
                                                                                                                                                                                                                'CXSE3.SA': 4.452076698415676, 'RANI3.SA': 2.740733329228567, 'PETR3.SA': 2.4718286785987735, 'RZAG11.SA': 4.483693811570158, 'VGIA11.SA': 4.4000199075794955, 'XPCA11.SA': 3.5274466670965516, 'KEPL3.SA': 0.3400377761663072, 'CAML3.SA': 4.129415464245886, 'KNCR11.SA': 2.744462121446814, 'FGAA11.SA': 2.0557931099253373, 'GGBR4.SA': 0.04076603944349195, 'GOAU3.SA': 1.081985312742024, 'KNCA11.SA': 3.763229373338091, 'CPLE3.SA': 0.5560547698503671, 'XPID11.SA': 3.812893347590073, 'ITUB3.SA': 4.268098338242091, 'BDIF11.SA': 3.7579138454550596, 'BTRA11.SA': 1.6242106132892817, 'HSLG11.SA': 1.0061710103938952, 'PATL11.SA': 2.720549996432234, 'VISC11.SA': 4.388421792696946, 'BBDC4.SA': 1.7845794018860452}}




print(f"Titulo: {item['Titulo']}")
print(f"Retorno: {round(item['Retorno'],2)}")
print(f"Risco: {round(item['Risco'],2)}")
print(f"Risco Ajustado: {round(item['RiscoAjustado'],2)}")
print(f"Sharpe: {round(item['Sharpe'],2)}")
print(f"Sortino: {round(item['Sortino'],2)}")

print()

print("Composição da Carteira")
for ticker, valor in item['Tickers'].items():
    print(f"{ticker}: {round(valor,2)}")

print()
print("\nComposição Ordenada")
for ticker, valor in sorted(item['Tickers'].items(), key=lambda x: x[1], reverse=True):
    print(f"{ticker}: {round(valor,2)}")

print()

print("\nComposição Ajustada")
tickers_ajustados = {ticker: valor *
                     2 for ticker, valor in item['Tickers'].items()}
for ticker, valor in tickers_ajustados.items():
    print(f"{ticker}: {round(valor,2)}")

print("\nComposição Ajustada Ordenada")
for ticker, valor in sorted(tickers_ajustados.items(), key=lambda x: x[1], reverse=True):
    print(f"{ticker}: {round(valor,2)}")

print("\n" + "-"*50 + "\n")
