T="$(date +%s)"
psql -U demo -d acsi7demo -c "UPDATE account_move SET partner_id = (SELECT DISTINCT partner_id FROM account_move_line WHERE account_move.id = account_move_line.move_id) WHERE EXISTS (SELECT DISTINCT partner_id FROM account_move_line where account_move.id = account_move_line.move_id)"
T="$(($(date +%s)-T))"
echo $T
