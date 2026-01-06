# Refactor: Split SitesOverview utils.ts into modular, organized files

Extract all functions and constants from the monolithic `client/jetpack-cloud/sections/agency-dashboard/sites-overview/utils.ts` file into separate, focused files organized by functionality and location of use. Improve i18n practices by replacing raw `translate` calls with `useTranslate` hooks.