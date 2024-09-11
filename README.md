# engeto-powerbi-project

**Projekt Engeto akademie: Datová vizualizace v Power BI**  
**Autor:** Markéta Svěráková Wallo  
**Email:** marketa.wallo@gmail.com  
**Discord:** marketasverakova_37252  
**GitHub Repozitář:** [github.com/MarketaSW/engeto-powerbi-project](https://github.com/MarketaSW/engeto-powerbi-project)

Cílem pátého projektu bylo vyzkoušet si práci v Power BI. Část dat byla dostupná pouze v pdf, bylo proto třeba napsat script v Pythonu pro scraping z webu a uložení do tabulky.

## Akutní respirační onemocnění v České Republice - sezóna 2023/2024

Tento repozitář obsahuje report v Power BI, zobrazující údaje o akutních respiračních onemocněních a pracovní neschopnosti. Data jsou vymezena časově na poslední epidemiologickou sezónu březen 2023 - březen 2024. Zobrazené údaje jsou přepočteny na 100 000 obyvatel České republiky.

## Soubory

- **`web_scraping/`**: Skript k získání podkladů ze stránek Státního zdravotního ústavu a související soubory.
- **`marketa-sverakova-wallo-report-ARI-PN.pbix`**: Hlavní soubor Power BI reportu.
- **`podklady_report/`**: Složka se zdrojovými daty k reportu.

## Návod k otevření

1. Naklonujte repozitář nebo stáhněte soubor `.pbix`.
2. Otevřete soubor `.pbix` pomocí Power BI Desktop.
3. Ujistěte se, že zdrojové datové soubory jsou umístěny v adresáři `data/` relativně k souboru `.pbix`.
4. Aktualizujte data v Power BI Desktop, aby se načetla nejnovější data ze zdrojových souborů.

## Zdroje dat

- **`podklady_report/ari_2022_23.xlsx`**: Data k akutním respiračním infekcím.
- **`podklady_report/ukazatele-pracovni-neschopnosti-podle-pohlavi-a-diagnozy`**: Data k pracovní neschopnosti dle skupin nemocí.
- **`podklady_report/ukazatele-pracovni-neschopnosti-podle-pohlavi-a-vekove-skupiny`**: Data k pracovní neschopnosti dle věkových skupin.
