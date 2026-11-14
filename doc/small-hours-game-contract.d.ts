// Typed reading of the Small Hours game plugin contract.
// Derived from upstream main @ afca56c (v2.24.3): src/engine/engine.js,
// src/games/registry.js, src/transport/host-view.js, public/js/game-api.js,
// games/README.md and games/_template/. Not an upstream file.
// "UNVERIFIED" marks shapes I did not trace to the code that consumes them.

/** Must be JSON-compatible: state and payloads cross the wire and are compared in tests. */
export type Json = null | boolean | number | string | Json[] | { [k: string]: Json };

export type PlayerId = string; // AI seats are "bot_1", "bot_2", ...

// ───────────── Server side: games/<id>/rules.js ─────────────

export interface GameEvent {
  type: string; // 'error' is special: the acting player sees `message` as a toast
  message?: string;
  [k: string]: Json | undefined;
}

export interface ActionResult<S> {
  state: S; // a new object; never mutate the input state
  events?: GameEvent[];
}

/** playerId is set by the server from the socket, never trusted from the client. */
export type ActionHandler<S, P = {}> = (
  state: S,
  payload: P & { playerId: PlayerId },
) => ActionResult<S>;

export interface EndResult {
  winner?: PlayerId | null;
  scores?: Record<PlayerId, number>;
  [k: string]: Json | undefined; // UNVERIFIED: extra fields a scoreboard may read
}

export interface Rules<S, V, C = Record<string, Json>> {
  setup(ctx: { players: PlayerId[]; config: C }): S;
  actions: Record<string, ActionHandler<S, any>>;
  /** Per-player view. Keys named my*, isMyTurn and manifest.privateKeys are stripped for the TV. */
  view(state: S, playerId: PlayerId): V;
  endIf(state: S): EndResult | null;
  /** Optional TV view; default is the first player's view minus the private keys. */
  hostView?(state: S): Json;
  /** Optional async step before setup, for fetched content (see games/quiz). UNVERIFIED return shape. */
  prepare?(config: C, ctx: Record<string, unknown>): Promise<unknown>;
}

// ───────────── Server side: games/<id>/index.js ─────────────

/** Bot: pure function, returns an action ({ type, ...payload }) or null to wait. */
export type BotChoose<S> = (state: S, botId: PlayerId) => ({ type: string } & Record<string, Json>) | null;

export interface AiOptions<S> {
  default: number; // AI seats when the lobby does not say
  max: number;
  cardsPerSeat?: number; // caps seats by deck size
  choose: BotChoose<S>;
  delay?(state: S): number | undefined; // ms before the bot moves
}

/** Checked at startup by manifestProblem(); a failing game is logged and skipped. */
export interface Manifest<S, V, C = Record<string, Json>> extends Rules<S, V, C> {
  id: string; // required, must equal the folder name
  label: string; // required
  min: number; // required integer
  max: number; // required integer, >= min
  icon?: string;
  blurb?: string;
  soloBlurb?: string;
  title?: string;
  order?: number; // lobby sort order, default 999
  hidden?: boolean; // keep out of the lobby while it has no screens
  music?: boolean; // play game music on the TV
  phases?: Record<string, number>; // phase name -> duration in ms, drives timers
  privateKeys?: string[]; // extra view keys the TV must not get
  ai?: AiOptions<S>;
  story?: unknown; // UNVERIFIED: intro shown on the TV
}

// ───────────── Wire ─────────────

/** Client -> server on /ws/player/:code (the TV uses /ws/host/:code). */
export interface GameActionMessage {
  type: 'GAME_ACTION';
  action: { type: string } & Record<string, Json>;
}

// ───────────── Browser side: games/<id>/client/*.js ─────────────
// Plain scripts using page globals: state, send, escapeHtml, showToast.

export interface PhonePlugin<V> {
  section: string; // element id of this game's block in phone.html
  render(msg: V): void;
  onEnter?(): void;
  reset?(): void;
  redraw?(): void; // after a resize, an error or a setting
  lobbyOptions?(): unknown; // UNVERIFIED
  startConfig?(): unknown; // UNVERIFIED
  startLabel?(): string; // UNVERIFIED
}

export interface TvPlugin<V> {
  render(msg: V): void;
  onEnter?(msg: V): void;
  onLeave?(msg: V): void;
  onMute?(muted: boolean): void;
  scoreboard?(
    msg: V,
    ctx: { names: unknown; ids: unknown; scores: unknown },
  ): { entries?: unknown; roundLabel?: string };
  alwaysScoreboard?: boolean;
}

export interface SH {
  registerGame<V>(id: string, plugin: PhonePlugin<V> | TvPlugin<V>): void;
  game(id: string): PhonePlugin<any> | TvPlugin<any> | null;
  duckMusic(): void;
  aiPersona(id: PlayerId): unknown | null;
}
