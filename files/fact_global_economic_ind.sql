BEGIN;
    CREATE TABLE IF NOT EXISTS etl_kaggle.fact_global_economic_ind (
        "country_id" int not NULL,
        "country" TEXT NULL,
        "year" int not NULL,
        "ama_exchange_rate" numeric NULL,
        "imf_based_exchange_rate" numeric NULL,
        "population" int NULL,
        "currency" TEXT NULL,
        "per_capita_gni" int NULL,
        "agriculture,hunting,forestry,fishing(isic_a_b)" numeric NULL,
        "changes_in_inventories" numeric NULL,
        "construction_(isic_f)" numeric NULL,
        "exports_of_goods_and_services" numeric NULL,
        "final_consumption_expenditure" numeric NULL,
        "general_government_final_consumption_expenditure" numeric NULL,
        "gross_capital_formation" numeric NULL,
        "gross_fixed_capital_formation" numeric NULL,
        "household_consumption_expenditure" numeric NULL,
        "imports_of_goods_and_services" numeric NULL,
        "manufacturing_(isic_d)" numeric NULL,
        "mining,_manufacturing,_utilities(isic_c_e)" numeric NULL,
        "other_activities_(isic_j_p)" numeric NULL,
        "total_value_added" numeric NULL,
        "transport,storage_and_communication(isic_i)" numeric NULL,
        "wholesale,retail_trade,restaurants_and_hotels(isic_g_h)" numeric NULL,
        "gross_national_income(gni)_in_usd" numeric NULL,
        "gross_domestic_product_(gdp)" numeric NULL

    );
COMMIT;
    