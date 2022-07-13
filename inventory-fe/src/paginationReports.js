const elementsXpage = 8;

let paginatedData = [];

function totalPages(listLength) {
  return Math.ceil(listLength / elementsXpage);
}

function getDataPage(page, data) {
  paginatedData = [];
  let start = page * elementsXpage - elementsXpage;
  let end = page * elementsXpage;

  paginatedData = data.slice(start, end);
  return paginatedData;
}

function getPreviousPage(page) {
  if (page > 1) {
    return page - 1;
  }
  return page;
}

function getNextPage(page, totalPages) {
  if (page < totalPages) {
    return page + 1;
  }
  return page;
}

export const paginationReports = {
  totalPages,
  getDataPage,
  getPreviousPage,
  getNextPage,
};
