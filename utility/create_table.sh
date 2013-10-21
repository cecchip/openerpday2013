psql -U demo -d acsi7demo -c "CREATE TABLE account_move_acsi As SELECT * FROM account_move;"
psql -U demo -d acsi7demo -c "CREATE TABLE res_partner_acsi As SELECT * FROM res_partner;"
