Bootstrap base components:

  - Use this in the base template as a block: http://getbootstrap.com/components/#page-header
  - Use these as basis for cards: http://getbootstrap.com/components/#thumbnails-custom-content
  - how to park elements? http://stackoverflow.com/questions/21301316/how-to-bootstrap-navbar-static-to-fixed-on-scroll

Done:

  - Bootstrap in stack
    - bower install
    - gulp, scss
    - vendor build (not source)
  - hard code top nav

Major task groups

  - Styles
    - Base typog
    - Heading typog
    - Color swatches
    - Logo
    - Topbar styles

  - CMS
    - add groups
  - Stubbed UI (stock bootstrap, hard coded content)
  - Scaffolding (real data)
    - skeleton content templates
  - Production
    - Basic deploy
    - Search (elasticsearch)
    - Redis caching
    - cron tasks (or similar):
      - search: update_index
      - publish_scheduled_pages
  - ocean story functionality/prototype (real data)
  - pull top nav menu items from CMS (?)
    - figure out how placing pages in the menus should work (with Jenny)
  - filter/search/view switch for cards
  - coupled Marine Planner instance

Lay out incremental goals for next week and the rest of Nov

  - ol3 map on OS pages
    - maybe render some data?

 - first pass:
   - stock OL3 (http://docs.openlayers.org/library/introduction.html)
 - openlayers 3
   - hosted, initially
   - will need to setup build env, likely
     - https://github.com/openlayers/ol3/blob/master/CONTRIBUTING.md
     - http://boundlessgeo.com/2014/02/openlayers-3-custom-builds/
   - bower
   - build

How to have full width media elements inside the content area?
http://stackoverflow.com/questions/24049467/how-to-create-a-100-screen-width-div-inside-a-container-in-bootstrap


Top nav Menu

    2nd level only?

    How to designate which menu a page goes in? (E)

Login item?

    "My MARCO +ICON"

Grid/list view

    what metadata fields in CMS to support filtering? (E)

Event page: look at comp, make sure CMS has all the fields (E)

    esp Address

groups need to be in beta in some form

summary: for beta, implement Join a group/public groups page, but not "My groups"

    dependency ordering with portal update?

    public group profiles, centrally administered for beta

    "this group elsewhere" field (with help text suggesting fb, goog, mailing lists, etc)

    linked to a marine planner group? (URL or id or something?)

    request to join (manual addition)
