import requests
from dotenv import load_dotenv
import os
import csv


load_dotenv()

store_name = os.getenv("STORE_NAME")
api_key =  os.getenv("KEY") 
secret_key = os.getenv("SECRET_KEY")
api_token = os.getenv("TOKEN") 

nonetypes = 0

def get_collections_with_product_counts_and_tags():
    url = f"https://{store_name}.myshopify.com/admin/api/2021-01/graphql.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": api_token, 
    }
    query = """
    {
      collections(first: 250) {
        edges {
          node {
            id
            title
            updatedAt
            ruleSet{
              appliedDisjunctively
              rules{
                column
                condition
                conditionObject
                relation
              }
            }
            image{
              url
              altText
              height
              width
            }
            seo{
              description
              title
            }
            productsCount
            products(first: 250) {
              edges {
                node {
                  tags
                  status
                }
              }
            }
          }
        }
      }
    }
    """
    response = requests.post(url, json={'query': query}, headers=headers)
    return response.json()

def main():
    try:
        data = get_collections_with_product_counts_and_tags()
        # print(data)
    except Exception as e:
        print(f"Error fetching data from Shopify {e}")
        
        return
    
    collections = data['data']['collections']['edges']
    
    collection_data = []


    for collection in collections:
        collection_node = collection['node']
        collection_id = collection_node['id']
        collection_title = collection_node['title']
        tags = set()


        product_count = collection_node['productsCount']


        active_product_count = 0
        archived_product_count = 0
        draft_product_count = 0

        for product in collection_node['products']['edges']:
            product_tags = product['node']['tags']
            match product['node']['status']:
              case 'ACTIVE':
                active_product_count += 1
              case 'ARCHIVED':
                archived_product_count += 1
              case 'DRAFT':
                draft_product_count += 1
            
            tags.update(product_tags)


        rules_list = []
        
        try:
          rules = collection_node['ruleSet']['rules']
          rules_list = [{'column': rule.get('column'), 'condition': rule.get('condition'), 'conditionObject': rule.get('conditionObject'), 'relation': rule.get('relation')} for rule in rules]
        except Exception as e:
          global nonetypes 
          nonetypes += 1

        collection_info = {
            'collection_id': collection_id,
            'collection_title': collection_title,
            'product_count': product_count,
            'active_count': active_product_count,
            'archived_count': archived_product_count,
            'draft_count': draft_product_count,
            'tags': list(tags),
            'rules': rules_list
        }
        collection_data.append(collection_info)
    
    # Write collection data to a CSV file
    with open('collections_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(['Collection ID', 'Collection Title', 'Rules', 'Product Count', 'Active Product Count', 'Draft Product Count', 'Archived Product Count',  'Tags'])
        
        for data in collection_data:
            if data["rules"] == []:
              rules_str = 'NULL'
            else:
              rules_str = '\n'.join([f"{rule['column']} {rule['relation']} {rule['condition']} " for rule in data['rules']])

            writer.writerow([data['collection_id'], data['collection_title'], rules_str, data['product_count'], data['active_count'], data['draft_count'], data['archived_count'], data['tags']])

    class col:
      HEADER = '\033[95m'
      OKBLUE = '\033[94m'
      OKCYAN = '\033[96m'
      OKGREEN = '\033[92m'
      WARNING = '\033[93m'
      FAIL = '\033[91m'
      ENDC = '\033[0m'
      BOLD = '\033[1m'
      UNDERLINE = '\033[4m'


    print(f"{col.HEADER}\n\nData written to collections_data.csv file successfully!")
    print(f"{col.HEADER}\nTotal collections without rules: {col.OKGREEN}{nonetypes}")
    print(f"{col.HEADER}\nTotal collections with rules: {col.OKGREEN}{len(collection_data) - nonetypes}")
    print(f"{col.HEADER}\nTotal collections: {col.OKGREEN}{len(collection_data)}")


if __name__ == "__main__":
    main()
