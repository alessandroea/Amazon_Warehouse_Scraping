# Amazon_Warehouse_Scraping

## This script aims to scrape Amazon Warehouse and send an email back if there are products whose price matches with the target one.



### The flow of this program:

1- Setting out the product to search for, the min/max budget for that.

2- Web scraping of Amazon Warehouse: the grabbed data is stored into amazonscraping_ws.csv.

3- Sorting the dataframe out.

4- Filtering the data in order to consider only those articles whose names contain exactly the typed product_to_search and whose prices are within the min/max budget.

5- Check of the final filtered_data: if it's empty, the programs returns "No result..." (no products within that range of price). Otherwise, it will execute the function sending_alert().

6- Deleting the created amazonscraping_ws.csv.
