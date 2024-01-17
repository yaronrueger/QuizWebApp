/// <reference types="vite/client" />
/// <reference types="vite-plugin-svgr/client" />

import { Url } from 'url';

interface ImportMetaEnv {
	readonly VITE_API_BASE_PATH: Url;
}

interface ImportMeta {
	readonly env: ImportMetaEnv;
}
