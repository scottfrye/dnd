import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('D:/temp/pioneer prices.csv')
    df.drop(labels='Sector', inplace=True, axis=1)
    df.dropna(subset='Star', inplace=True)
    df.set_index('Star', inplace=True)
    df = df[[c for c in df.columns if 'Unnamed' not in c]]
    df = df[df.columns[:]].replace('[\$,]', '', regex=True)  # get rid of all the dollar signs
    df = df[df.columns[:]].replace('[\),]', '', regex=True)  # remove closing parenths
    df = df[df.columns[:]].replace('[\(,]', '-', regex=True)  # replace open parenths with neg sign
    # df[['Grain', 'Air Processors']].apply(pd.to_numeric)
    df = df[list(df.columns)].apply(pd.to_numeric)

    all_systems = list(df.index.values)

    all_results = []
    for system_1 in all_systems:
        for system_2 in all_systems:
            # print(f'from {system_1} to {system_2}:')
            if system_1 == system_2:
                continue
            else:
                diff_rows = df.loc[system_1].compare(df.loc[system_2])
                diff_rows['price_diff'] = diff_rows['other'] - diff_rows['self']
                max_row = diff_rows[diff_rows['price_diff'] == diff_rows['price_diff'].max()]['price_diff']
                commodity = max_row.index.values[0]
                price_diff = max_row.values[0]
                print(
                    f'{system_1} to {system_2}: commodity: {max_row.index.values[0]} for profit of {max_row.values[0]:.2f}')
                all_results.append([system_1, system_2, commodity, price_diff])

    # df[df.columns[1:]] = df[df.columns[1:]].replace('[\$,]', '', regex=True).astype(float)
    df_rets = pd.DataFrame(all_results, columns=['from', 'to', 'commodity', 'return']).sort_values('return',
                                                                                                   ascending=False)
    df_rets.to_csv('d:/temp/pioneer_returns.csv')
    print('Done.')
