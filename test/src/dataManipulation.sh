
hosp=(MidTwnUrgentC^2231231234^NPI BgCtyChldrnUrgntCar^1231231234^NPI SmvUrgentC^3231231234^NPI WstrnRgnlMedCntr^1231231235^NPI PacNWHosED^2481227981^NPI MidWsUnvMC^6462583641^NPI SthrnMdwstMedCntr^1231231236^NPI LakeMichMC^9879874000^NPI)

# make changes line by line
while read line; do
    randhosp=${hosp[$RANDOM % ${#hosp[@]} ]}
    echo $line | sed "s/G|G|G|G/G|${randhosp}|G|G/g"
done < hl7_records.txt
