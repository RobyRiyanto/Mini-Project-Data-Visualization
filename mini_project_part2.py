# Import library
import datetime
import pandas as pd
import matplotlib.pyplot as plt

class MiniProject_Dqlab:
    def __init__(self, link, data):
        self.link = link
        self.data = data

    def data_preparation(self):
        # Baca data
        dataset = pd.read_csv(self.link)
        
        # Buat kolom baru yang bertipe datetime dalam format '%Y-%m'
        dataset['order_month'] = dataset['order_date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").strftime('%Y-%m'))
        
        # Buat Kolom GMV
        dataset['gmv'] = dataset['item_price']*dataset['quantity']

        # Buat variabel untuk 5 propinsi dengan GMV tertinggi
        top_provinces = (dataset.groupby('province')['gmv']
                                .sum()
                                .reset_index()
                                .sort_values(by = 'gmv', ascending = False)
                                .head(5))

        # Buat satu kolom lagi di dataset dengan nama province_top dengan value 5 propinsi GMV tertinggi, sisanya 'other'
        dataset['province_top'] = dataset['province'].apply(lambda x: x if(x in top_provinces['province'].to_list()) else 'other')
        
        # Save to CSV
        dataset.to_csv(self.data, index = False, header = True)
        print('Data berhasil disimpan !!!')

    def case_1(self):
        dataset = pd.read_csv(self.data)
        
        # Mengambil informasi top 5 brands berdasarkan quantity
        top_brands = (dataset[dataset['order_month'] == '2019-12'].groupby('brand')['quantity'].sum().reset_index().sort_values(by = 'quantity', ascending = False).head(5))

        # Membuat dataframe baru, filter hanya di bulan Desember 2019 dan hanya top 5 brands
        dataset_top5brand_dec = dataset[(dataset['order_month'] == '2019-12') & (dataset['brand'].isin(top_brands['brand'].to_list()))]

        # Print top brands
        print('Top 5 Brands :')
        print(top_brands)
        
        self.top5brand_dec = dataset_top5brand_dec

    def case_2(self):
        self.top5brand_dec.groupby(['order_date','brand'])['quantity'].sum().unstack().plot(marker = '.', cmap = 'plasma')
        plt.title('Daily Sold Quantity Dec 2019 - Breakdown by Brands',loc = 'center',pad = 30, fontsize = 15, color = 'blue')
        plt.xlabel('Order Date', fontsize = 12)
        plt.ylabel('Quantity',fontsize = 12)
        plt.grid(color = 'darkgray', linestyle = ':', linewidth = 0.5)
        plt.ylim(ymin = 0)
        plt.legend(loc = 'upper center', bbox_to_anchor = (1.1, 1), shadow = True, ncol = 1)
        plt.annotate('Terjadi lonjakan', xy = (7, 310), xytext = (8, 300),
                    weight = 'bold', color = 'red',
                    arrowprops = dict(arrowstyle = '->',
                                    connectionstyle = "arc3",
                                    color = 'red'))
        plt.gcf().set_size_inches(10, 5)
        plt.tight_layout()
        plt.show()

    def case_3(self):
        plt.clf()
        self.top5brand_dec.groupby('brand')['product_id'].nunique().sort_values(ascending = False).plot(kind = 'bar', color = 'green')
        plt.title('Number of Sold Products per Brand, December 2019',loc = 'center',pad = 30, fontsize = 15, color = 'blue')
        plt.xlabel('Brand', fontsize = 15)
        plt.ylabel('Number of Products', fontsize = 15)
        plt.ylim(ymin = 0)
        plt.xticks(rotation = 0)
        plt.show()

    def case_4(self):
        # Membuat dataframe baru, untuk agregat jumlah quantity terjual per product
        dataset_top5brand_dec_per_product = self.top5brand_dec.groupby(['brand','product_id'])['quantity'].sum().reset_index()

        # Beri kolom baru untuk menandai product yang terjual >= 100 dan <100
        dataset_top5brand_dec_per_product['quantity_group'] = dataset_top5brand_dec_per_product['quantity'].apply(lambda x: '>= 100' if x >= 100 else '< 100')
        dataset_top5brand_dec_per_product.sort_values('quantity', ascending = False, inplace = True)

        # Membuat referensi pengurutan brand berdasarkan banyaknya semua product
        s_sort = dataset_top5brand_dec_per_product.groupby('brand')['product_id'].nunique().sort_values(ascending = False)

        # Plot stacked barchart
        dataset_top5brand_dec_per_product.groupby(['brand', 'quantity_group'])['product_id'].nunique().reindex(index = s_sort.index, level = 'brand').unstack().plot(kind = 'bar', stacked = True)
        plt.title('Number of Sold Products per Brand, December 2019', loc = 'center', pad = 30, fontsize = 15, color = 'blue')
        plt.xlabel('Brand', fontsize = 15)
        plt.ylabel('Number of Products',fontsize = 15)
        plt.ylim(ymin = 0)
        plt.xticks(rotation = 0)
        plt.show()

    def case_5(self):
        plt.figure(figsize = (10, 5))
        plt.hist(self.top5brand_dec.groupby('product_id')['item_price'].median(), 
                bins = 10, 
                stacked = True, 
                range = (1, 2000000), 
                color = 'green')
        plt.title('Distribution of Price Median per Product\nTop 5 Brands in Dec 2019', fontsize = 15, color = 'blue')
        plt.xlabel('Price Median', fontsize = 12)
        plt.ylabel('Number of Products', fontsize = 12)
        plt.xlim(xmin = 0, xmax = 2000000)
        labels, locations = plt.xticks()
        plt.xticks(labels, (labels).astype(int))
        plt.show()

    def case_6a(self):
        #agregat per product
        data_per_product_top5brand_dec = self.top5brand_dec.groupby('product_id').agg({'quantity': 'sum', 
                                                                                        'gmv':'sum', 
                                                                                        'item_price':'median'}).reset_index()

        #scatter plot
        plt.figure(figsize = (10, 8))
        plt.scatter(data_per_product_top5brand_dec['quantity'],data_per_product_top5brand_dec['gmv'], marker = '+', color = 'red')
        plt.title('Correlation of Quantity and GMV per Product\nTop 5 Brands in December 2019', fontsize = 15, color = 'blue')
        plt.xlabel('Quantity', fontsize = 12)
        plt.ylabel('GMV (in Millions)', fontsize = 12)
        plt.xlim(xmin = 0, xmax = 300)
        plt.ylim(ymin = 0, ymax = 200000000)
        labels, locations = plt.yticks()
        plt.yticks(labels, (labels/1000000).astype(int))
        plt.show()

    def case_6b(self):
        # plt.clf()
        #agregat per product
        data_per_product_top5brand_dec = self.top5brand_dec.groupby('product_id').agg({'quantity': 'sum', 
                                                                                        'gmv':'sum', 
                                                                                        'item_price':'median'}).reset_index()

        #scatter plot
        plt.figure(figsize = (10,8))
        plt.scatter(data_per_product_top5brand_dec['item_price'], 
                    data_per_product_top5brand_dec['quantity'], 
                    marker  = 'o', 
                    color = 'green')
        plt.title('Correlation of Quantity and GMV per Product\nTop 5 Brands in December 2019', fontsize = 15, color = 'blue')
        plt.xlabel('Price Median', fontsize = 12)
        plt.ylabel('Quantity', fontsize = 12)
        plt.xlim(xmin = 0, xmax = 2000000)
        plt.ylim(ymin = 0, ymax = 250)
        labels, locations = plt.xticks()
        plt.xticks(labels, (labels).astype(int))
        plt.show()

link = 'https://dqlab-dataset.s3-ap-southeast-1.amazonaws.com/retail_raw_reduced.csv'
data = 'retail_raw_reduced_final.csv'

app = MiniProject_Dqlab(link, data)
app.data_preparation()
app.case_1()
app.case_2()
app.case_3()
app.case_4()
app.case_5()
app.case_6a()
app.case_6b()