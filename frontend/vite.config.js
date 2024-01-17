import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},
	server: {
		proxy: {
			// Does currently not work:
			'^/api': {
				target: 'https://jan-ehehalt.de',
				changeOrigin: true
			}
		}
	}
};

export default config;
