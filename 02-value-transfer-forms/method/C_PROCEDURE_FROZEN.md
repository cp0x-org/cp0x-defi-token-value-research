# Замороженная C-процедура по universe (stage 3)

Заморожена: 2026-10-03T18:05:11Z
Universe: data/stage3_universe_frozen.csv, sha256 начинается с d4556a803bd1e7f1, 164 протокола, не меняется.

Один запрос на протокол, имя протокола подставляется в начало без изменения остального текста:
"<name> stakers previously earned ETH rewards now receive native token bought back from market rewards change protocol switched reward currency"

Для каждого протокола одинаково фиксируются: old mechanism, new mechanism, transition (да/нет/неясно), source quality, C yes/no/unclear.
Точные даты решений и активаций устанавливаются отдельным фактчеком по существующим правилам реестра, не этой процедурой.
Никаких дополнительных запросов под отдельные кейсы не добавляется.

Калибровка: положительные контроли из universe GMX (30.10.2024, восстановлены все четыре шага) и Gains (июль 2024, восстановлены форма до как direct revenue sharing, форма после как buyback and distribute, переход; день по процедуре не восстанавливается и устанавливается фактчеком). Шаблон ранее прошёл безымянный контроль GMX в разделе 32.
