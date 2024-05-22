# Shopify Collection Exporter

Simple Shopify Collection to CSV for Python utilizing the GraphQL API. Written in a pinch, so the code sucks, but doesn't it all...

Documentation: https://shopify.dev/docs/api/admin-graphql/2023-07/objects/collection

I needed to get collections data from a shopify store before an 11am meeting. The fact that there is no export button is both annoying and reassuring, as it keeps us devs around. 

Maybe I'll make it something a bit more installable, but at the moment this is just a quick script that I thought would be fun to share.

The graphql query is not comprehensive to possible collection schema as per Shopify Documentation. To update this, manually change that and the csv parsing.

## Usage

- Clone the repo
- Install the requirements
    if you have an environment initialized: 
    ```bash
    pip install -r requirements.txt 
    ```
    or initialize a conda environment
    ```bash
    conda create --name collection_get --file requirements.txt 
    ```
- Initialize a private app on Shopify
- Update .env file with your Shopify store and access token
- Update the query in collection-get.py to your liking according to the docs above
- Update the csv parser manually (sorry)
- Run the script
    ```bash
    python collection-get.py
    ```

You should see a csv file with the collections in the root directory.

MAKE SURE TO NOT SHARE YOUR ACCESS TOKEN!
Be safe and don't do anything stupid with fire.
