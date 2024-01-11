# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 11:17:00 2023

@author: Cyrus

Target list input examples

{
	"target_list":
	{
		"target_id":
		{
			"1":
			{
				"target_type":"primary",
				"target_high": 511,
				"target_low": 471,
				"reward_continvency_type":"target"
			},
			"2":
			{
				"target_type":"primary",
				"target_high": 552,
				"target_low": 512,
				"reward_continvency_type":"target"
			},
			"3":
			{
				"target_type":"background",
				"background_style":"high_low",
				"target_high": 140,
				"target_low": 100
			},
            "4":
			{
				"target_type":"background",
				"background_style":"random",
				"no_of_phenotypes": 400
			},
			"5":
			{
				"target_type":"background",
				"background_style":"background_generator",
				"background_generator_settings":
				{
    				"generator_type":"max_mean_std_nonsequential_post_screening",
                    "screen_out_equal_or_less":1,
                    "remove_avg_hamming_equal_or_less":null,
                    "remove_std_hamming_equal_or_greater":0.8,
                    "removal_function_type":"percentage",
    				"number_of_nonsequential_targets":2,
                    "nonsequential_background_target_size":40,
                    "number_of_continuous_targets":2,
                    "continuous_background_target_length":40
				}
			}
		}
    }
}
"""