#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:52:15 2019

@author: Reza
"""

def preprocessing(dataframes):
    ''' foods table '''
    # Create a copy of table and then drop unnecessary columns, 
    # replace "id" with "food_id", and try to fill the missing data. 
    df_0 = dataframes[0].copy()
    df_0.drop(["created_at","updated_at"], axis=1, inplace=True)
    df_0.rename(columns={'id': 'food_id'}, inplace=True)

    # Fill availability cell with one of its children data (here with the 1st one)
    ancestry_id = df_0[df_0.availability.isnull()].food_id
    child_indexs = df_0[df_0.ancestry == str(ancestry_id.values[0])].index
    ancestry_index = df_0[df_0.availability.isnull()].index
    df_0.loc[ancestry_index[0], ["availability"]] = df_0.loc[child_indexs[0], ["availability"]]

    # Fill the category_id with the value of "semoule"
    index_num = df_0[df_0.category_id.isnull()].index
    df_0.loc[index_num[0], ["category_id"]] = df_0[df_0.name == "semoule"]["category_id"].values[0]

    # Change the ancestry value with the subcategory id number
    sub_cat = df_0[df_0.ancestry == "510/404"]["ancestry"]
    df_0.loc[sub_cat.index, "ancestry"] = sub_cat.values[0].split("/")[1]

    # Repeat the same procedure for other values
    df_0.loc[[189,321], "ancestry"] = "512"
    df_0.loc[[329,521], "ancestry"] = "508"

    # Change the "NaN" value in ancestry column with "1" (to be considered 
    # as a root position) for the foods line with at least one child in the table.
    # And those that don't have any (parent/child) relation with "0".
    id_list = df_0[df_0.ancestry.isnull()].index
    for i in id_list:
        if len(df_0[df_0.ancestry == str(df_0.loc[i, "food_id"])]) > 0:
            df_0.loc[i, "ancestry"] = "1"
        else:
            df_0.loc[i, "ancestry"] = "0"
    
    df_0.category_id = df_0.category_id.astype(int)
    df_0.ancestry = df_0.ancestry.astype(int)

    ''' items table '''
    df_1 = dataframes[1].copy()
    df_1.drop(["Quantity"], axis=1, inplace=True)
    df_1.columns = ['id', 'recipe-ingredient', 'name_food', 'title_recipe', 'ingredients_recipe', 'origin_recipe']
    df_1.set_index("id", inplace=True)
        
    ''' recipes table '''
    df_2 = dataframes[2].copy()
    df_2.drop(["recommendable","status"], axis=1, inplace=True)
    df_2.rename(columns={'id': 'recipe_id'}, inplace=True)

    # Add the Mama web link recipes for the missing values in the "link" column
    foodmama_path = "https://www.foodmama.fr/recipes/"
    index_list = df_2[df_2.link.isnull()].index
    for i in index_list:
        df_2.loc[i, ["link"]] = foodmama_path + str(df_2.loc[i, ["recipe_id"]].values[0])
    
    # Replace "NaN" values with "unknown" rating
    df_2.rating.fillna("unknown", inplace=True)

    return df_0, df_1, df_2
