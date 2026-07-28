| Dataset            | Primary Source | Backup Source | Collection Method            | Raw Format | Processed Format | Update Frequency          | Priority | Status      |
|--------------------|----------------|---------------|------------------------------|------------|------------------|---------------------------|----------|-------------|
| Teams              | Wikipedia      | FIFA          | `pandas.read_html()`         | HTML       | CSV              | Before tournament         | High     | ⏳ Pending |
| Squads             | Wikipedia      | FIFA          | `pandas.read_html()`         | HTML       | CSV              | When announced            | High     | ⏳ Pending |
| Groups             | Wikipedia      | FIFA          | `pandas.read_html()`         | HTML       | CSV              | Before tournament         | High     | ⏳ Pending |
| Stadiums           | Wikipedia      | FIFA          | `pandas.read_html()`         | HTML       | CSV              | Rare updates              | Medium   | ⏳ Pending |
| Match Schedule     | FIFA           | Wikipedia     | BeautifulSoup / `read_html()`| HTML       | CSV              | When fixtures change      | High     | ⏳ Pending |
| Match Results      | FIFA           | Wikipedia     | BeautifulSoup / `read_html()`| HTML       | CSV              | After every match         | High     | ⏳ Pending |
| Group Standings    | FIFA           | Wikipedia     | `pandas.read_html()`         | HTML       | CSV              | After each matchday       | High     | ⏳ Pending |
| Team Statistics    | FBref          | FIFA          | `pandas.read_html()`         | HTML       | CSV              | After every match         | High     | ⏳ Pending |
| Player Statistics  | FBref          | FIFA          | `pandas.read_html()`         | HTML       | CSV              | After every match         | High     | ⏳ Pending |
| Match Statistics   | FBref          | FIFA          | `pandas.read_html()`         | HTML       | CSV              | After every match         | High     | ⏳ Pending |
| Event Data         | StatsBomb      | —             | JSON download + Python       | JSON       | CSV / MySQL      | When available            | Medium   | ⏳ Pending |
| Referees           | FIFA           | Wikipedia     | Python                       | HTML       | CSV              | After appointments        | Low      | ⏳ Pending |