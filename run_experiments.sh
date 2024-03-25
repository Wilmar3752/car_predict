echo 'Setting all experiments'
dvc exp run -S 'feature_engineering.rarelabel_tol=0.01,0.1' \
            -S 'feature_engineering.scaler_method=standard,minmax' \
            -S 'feature_engineering.test_size=0.1' \
            --queue
echo 'Running all queued experiments'
dvc queue start
#echo 'Show all experiments by r2'
#dvc exp show --sort-by r2 --sort-order desc