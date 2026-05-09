import React, {useEffect, useMemo, useState} from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './CsvDataTable.module.css';

type SortState = {
  column: string;
  direction: 'asc' | 'desc';
};

type CsvDataTableProps = {
  src: string;
  label: string;
  initialPageSize?: number;
  maxRows?: number;
};

function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = '';
  let quoted = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];

    if (quoted) {
      if (char === '"' && next === '"') {
        field += '"';
        i += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        field += char;
      }
      continue;
    }

    if (char === '"') {
      quoted = true;
    } else if (char === ',') {
      row.push(field);
      field = '';
    } else if (char === '\n') {
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
    } else if (char !== '\r') {
      field += char;
    }
  }

  if (field || row.length) {
    row.push(field);
    rows.push(row);
  }

  return rows;
}

async function readResponseText(response: Response): Promise<string> {
  if (!response.body || !response.url.endsWith('.gz')) {
    return response.text();
  }

  if ('DecompressionStream' in window) {
    const stream = response.body.pipeThrough(new DecompressionStream('gzip'));
    return new Response(stream).text();
  }

  throw new Error('This browser cannot read gzip-compressed CSV files.');
}

export default function CsvDataTable({
  src,
  label,
  initialPageSize = 10,
  maxRows,
}: CsvDataTableProps): React.ReactElement {
  const csvUrl = useBaseUrl(src);
  const [headers, setHeaders] = useState<string[]>([]);
  const [rows, setRows] = useState<string[][]>([]);
  const [query, setQuery] = useState('');
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(initialPageSize);
  const [sort, setSort] = useState<SortState | null>(null);
  const [status, setStatus] = useState('Loading table...');
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;

    async function loadCsv() {
      try {
        setStatus('Loading table...');
        setError('');
        const response = await fetch(csvUrl);
        if (!response.ok) {
          throw new Error(`Unable to load ${csvUrl}: ${response.status}`);
        }
        const text = await readResponseText(response);
        const parsed = parseCsv(text.trim());
        if (!parsed.length) {
          throw new Error(`No rows found in ${csvUrl}`);
        }
        if (!cancelled) {
          setHeaders(parsed[0]);
          setRows(parsed.slice(1, maxRows ? maxRows + 1 : undefined));
          setStatus('');
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : String(err));
          setStatus('');
        }
      }
    }

    loadCsv();

    return () => {
      cancelled = true;
    };
  }, [csvUrl, maxRows]);

  useEffect(() => {
    setPage(0);
  }, [query, pageSize, sort]);

  const filteredRows = useMemo(() => {
    const needle = query.trim().toLowerCase();
    const filtered = needle
      ? rows.filter((row) => row.some((value) => value.toLowerCase().includes(needle)))
      : rows;

    if (!sort) {
      return filtered;
    }

    const index = headers.indexOf(sort.column);
    if (index < 0) {
      return filtered;
    }

    return [...filtered].sort((a, b) => {
      const av = a[index] ?? '';
      const bv = b[index] ?? '';
      const numericA = Number(av);
      const numericB = Number(bv);
      const bothNumeric = av !== '' && bv !== '' && !Number.isNaN(numericA) && !Number.isNaN(numericB);
      const result = bothNumeric
        ? numericA - numericB
        : av.localeCompare(bv, undefined, {numeric: true, sensitivity: 'base'});
      return sort.direction === 'asc' ? result : -result;
    });
  }, [headers, query, rows, sort]);

  const pageCount = Math.max(1, Math.ceil(filteredRows.length / pageSize));
  const currentPage = Math.min(page, pageCount - 1);
  const visibleRows = filteredRows.slice(currentPage * pageSize, currentPage * pageSize + pageSize);

  function toggleSort(column: string) {
    setSort((previous) => {
      if (!previous || previous.column !== column) {
        return {column, direction: 'asc'};
      }
      if (previous.direction === 'asc') {
        return {column, direction: 'desc'};
      }
      return null;
    });
  }

  if (error) {
    return <p className={styles.error}>{error}</p>;
  }

  return (
    <div>
      <div className={styles.toolbar}>
        <input
          className={styles.search}
          type="search"
          placeholder={`Search ${label}`}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        <select
          className={styles.pageSize}
          value={pageSize}
          onChange={(event) => setPageSize(Number(event.target.value))}>
          {[10, 25, 50, 100].map((value) => (
            <option key={value} value={value}>
              {value} rows
            </option>
          ))}
        </select>
        <span className={styles.summary}>
          {status ||
            `${filteredRows.length.toLocaleString()} of ${rows.length.toLocaleString()} displayed rows${
              maxRows ? ` (limited to first ${maxRows.toLocaleString()})` : ''
            }`}
        </span>
      </div>

      <div className={styles.tableWrap}>
        <table className={styles.table}>
          <thead>
            <tr>
              {headers.map((header) => (
                <th key={header} onClick={() => toggleSort(header)} title={`Sort by ${header}`}>
                  {header}
                  {sort?.column === header ? (sort.direction === 'asc' ? ' ▲' : ' ▼') : ''}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {visibleRows.map((row, rowIndex) => (
              <tr key={`${currentPage}-${rowIndex}`}>
                {headers.map((header, columnIndex) => (
                  <td key={header}>{row[columnIndex] ?? ''}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className={styles.pager}>
        <button className={styles.button} type="button" disabled={currentPage === 0} onClick={() => setPage(0)}>
          First
        </button>
        <button
          className={styles.button}
          type="button"
          disabled={currentPage === 0}
          onClick={() => setPage((value) => Math.max(0, value - 1))}>
          Previous
        </button>
        <span className={styles.summary}>
          Page {currentPage + 1} of {pageCount}
        </span>
        <button
          className={styles.button}
          type="button"
          disabled={currentPage >= pageCount - 1}
          onClick={() => setPage((value) => Math.min(pageCount - 1, value + 1))}>
          Next
        </button>
        <button
          className={styles.button}
          type="button"
          disabled={currentPage >= pageCount - 1}
          onClick={() => setPage(pageCount - 1)}>
          Last
        </button>
      </div>
    </div>
  );
}
