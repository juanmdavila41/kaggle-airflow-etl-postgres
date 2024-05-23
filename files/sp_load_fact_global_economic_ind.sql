-- ================================================
-- Template generated from Template Explorer using:
-- Create Procedure (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- This block of comments will not be included in
-- the definition of the procedure.
-- ================================================

CREATE OR REPLACE PROCEDURE etl_kaggle.sp_load_fact_global_economic_ind()
LANGUAGE plpgsql
AS $$
BEGIN
    WITH src AS (
        SELECT
            "country_id",
            "country",
            "year",
            "ama_exchange_rate",
            "imf_based_exchange_rate",
            "population",
            "currency",
            "per_capita_gni",
            "agriculture,hunting,forestry,fishing(isic_a_b)",
            "changes_in_inventories",
            "construction_(isic_f)",
            "exports_of_goods_and_services",
            "final_consumption_expenditure",
            "general_government_final_consumption_expenditure",
            "gross_capital_formation",
            "gross_fixed_capital_formation",
            "household_consumption_expenditure",
            "imports_of_goods_and_services",
            "manufacturing_(isic_d)",
            "mining,_manufacturing,_utilities(isic_c_e)",
            "other_activities_(isic_j_p)",
            "total_value_added",
            "transport,storage_and_communication(isic_i)",
            "wholesale,retail_trade,restaurants_and_hotels(isic_g_h)",
            "gross_national_income(gni)_in_usd",
            "gross_domestic_product_(gdp)"

        FROM tmp_global_economic_ind
    )
    INSERT INTO fact_global_economic_ind (
        "country_id",
        "country",
        "year",
        "ama_exchange_rate",
        "imf_based_exchange_rate",
        "population",
        "currency",
        "per_capita_gni",
        "agriculture,hunting,forestry,fishing(isic_a_b)",
        "changes_in_inventories",
        "construction_(isic_f)",
        "exports_of_goods_and_services",
        "final_consumption_expenditure",
        "general_government_final_consumption_expenditure",
        "gross_capital_formation",
        "gross_fixed_capital_formation",
        "household_consumption_expenditure",
        "imports_of_goods_and_services",
        "manufacturing_(isic_d)",
        "mining,_manufacturing,_utilities(isic_c_e)",
        "other_activities_(isic_j_p)",
        "total_value_added",
        "transport,storage_and_communication(isic_i)",
        "wholesale,retail_trade,restaurants_and_hotels(isic_g_h)",
        "gross_national_income(gni)_in_usd",
        "gross_domestic_product_(gdp)"

    )
    SELECT 
    "country_id",
    "country",
    "year",
    "ama_exchange_rate",
    "imf_based_exchange_rate",
    "population",
    "currency",
    "per_capita_gni",
    "agriculture,hunting,forestry,fishing(isic_a_b)",
    "changes_in_inventories",
    "construction_(isic_f)",
    "exports_of_goods_and_services",
    "final_consumption_expenditure",
    "general_government_final_consumption_expenditure",
    "gross_capital_formation",
    "gross_fixed_capital_formation",
    "household_consumption_expenditure",
    "imports_of_goods_and_services",
    "manufacturing_(isic_d)",
    "mining,_manufacturing,_utilities(isic_c_e)",
    "other_activities_(isic_j_p)",
    "total_value_added",
    "transport,storage_and_communication(isic_i)",
    "wholesale,retail_trade,restaurants_and_hotels(isic_g_h)",
    "gross_national_income(gni)_in_usd",
    "gross_domestic_product_(gdp)"

    FROM src
    ON CONFLICT (
        "country_id",
        "country",
        "year"
        ) DO UPDATE
    SET 
    a."country_id" = b."country_id",
    a."country" = b."country",
    a."year" = b."year",
    a."ama_exchange_rate" = b."ama_exchange_rate",
    a."imf_based_exchange_rate" = b."imf_based_exchange_rate",
    a."population" = b."population",
    a."currency" = b."currency",
    a."per_capita_gni" = b."per_capita_gni",
    a."agriculture,hunting,forestry,fishing(isic_a_b)" = b."agriculture,hunting,forestry,fishing(isic_a_b)",
    a."changes_in_inventories" = b."changes_in_inventories",
    a."construction_(isic_f)" = b."construction_(isic_f)",
    a."exports_of_goods_and_services" = b."exports_of_goods_and_services",
    a."final_consumption_expenditure" = b."final_consumption_expenditure",
    a."general_government_final_consumption_expenditure" = b."general_government_final_consumption_expenditure",
    a."gross_capital_formation" = b."gross_capital_formation",
    a."gross_fixed_capital_formation" = b."gross_fixed_capital_formation",
    a."household_consumption_expenditure" = b."household_consumption_expenditure",
    a."imports_of_goods_and_services" = b."imports_of_goods_and_services",
    a."manufacturing_(isic_d)" = b."manufacturing_(isic_d)",
    a."mining,_manufacturing,_utilities(isic_c_e)" = b."mining,_manufacturing,_utilities(isic_c_e)",
    a."other_activities_(isic_j_p)" = b."other_activities_(isic_j_p)",
    a."total_value_added" = b."total_value_added",
    a."transport,storage_and_communication(isic_i)" = b."transport,storage_and_communication(isic_i)",
    a."wholesale,retail_trade,restaurants_and_hotels(isic_g_h)" = b."wholesale,retail_trade,restaurants_and_hotels(isic_g_h)",
    a."gross_national_income(gni)_in_usd" = b."gross_national_income(gni)_in_usd",
    a."gross_domestic_product_(gdp)" = b."gross_domestic_product_(gdp)"

    ;
END;
$$;
    