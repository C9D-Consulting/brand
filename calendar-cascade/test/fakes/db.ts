// Just enough of the supabase-js query builder, over in-memory tables, to run
// the reconciler for real in tests.

type Row = Record<string, any>;
type Filter = (r: Row) => boolean;

export class FakeDb {
  tables: Record<string, Row[]> = { calendars: [], rules: [], mirrors: [], activity: [], google_accounts: [] };
  private seq = 0;

  from(table: string) {
    return new Query(this, table);
  }

  rpc() {
    return Promise.resolve({ data: true, error: null });
  }

  nextId() {
    return `row-${++this.seq}`;
  }
}

class Query {
  private filters: Filter[] = [];
  private op: 'select' | 'insert' | 'update' | 'delete' | 'upsert' = 'select';
  private payload: any;
  private mode: 'many' | 'single' | 'maybe' = 'many';
  private window?: [number, number];

  constructor(private db: FakeDb, private table: string) {}

  select() {
    return this;
  }
  insert(rows: Row | Row[]) {
    this.op = 'insert';
    this.payload = Array.isArray(rows) ? rows : [rows];
    return this;
  }
  update(patch: Row) {
    this.op = 'update';
    this.payload = patch;
    return this;
  }
  delete() {
    this.op = 'delete';
    return this;
  }
  eq(col: string, v: unknown) {
    this.filters.push((r) => r[col] === v);
    return this;
  }
  gt(col: string, v: string) {
    this.filters.push((r) => r[col] > v);
    return this;
  }
  in(col: string, vs: unknown[]) {
    this.filters.push((r) => vs.includes(r[col]));
    return this;
  }
  order() {
    return this;
  }
  limit() {
    return this;
  }
  range(from: number, to: number) {
    this.window = [from, to + 1];
    return this;
  }
  single() {
    this.mode = 'single';
    return this;
  }
  maybeSingle() {
    this.mode = 'maybe';
    return this;
  }

  private run(): any {
    const rows = this.db.tables[this.table];
    const match = (r: Row) => this.filters.every((f) => f(r));
    let out: Row[];
    if (this.op === 'insert') {
      out = this.payload.map((r: Row) => ({ id: this.db.nextId(), ...r }));
      rows.push(...out);
    } else if (this.op === 'update') {
      out = rows.filter(match);
      out.forEach((r) => Object.assign(r, this.payload));
    } else if (this.op === 'delete') {
      out = rows.filter(match);
      this.db.tables[this.table] = rows.filter((r) => !match(r));
    } else {
      out = rows.filter(match);
    }
    if (this.window) out = out.slice(...this.window);
    out = out.map((r) => ({ ...r }));
    if (this.mode === 'many') return out;
    return out[0] ?? null;
  }

  then(ok?: (v: { data: any; error: null }) => unknown, fail?: (e: unknown) => unknown) {
    return Promise.resolve({ data: this.run(), error: null }).then(ok, fail);
  }
}
