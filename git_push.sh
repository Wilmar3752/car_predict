echo "agregando archivos necesarios"
git add -f models/final_pipeline.joblib
echo "Realizando commit"
git commit -m "Feat: New release of car_predict"
echo "Haciendo push"
git push origin master
echo "stop tracking"
git rm --cached -r models/final_pipeline.joblib