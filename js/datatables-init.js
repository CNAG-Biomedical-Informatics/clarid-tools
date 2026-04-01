// docs/js/dt-init.js
(function () {
  function enhance() {
    $('table.datatable, div.datatable table').each(function () {
      if (!$.fn.dataTable.isDataTable(this)) {
        $(this).DataTable({
          pageLength: 10,
          ordering: true,
          deferRender: true
        });
      }
    });
  }

  if (document.readyState !== 'loading') enhance();
  else document.addEventListener('DOMContentLoaded', enhance);

  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(enhance); // MkDocs Material instant nav
  }
})();
