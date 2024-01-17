<script lang="ts">
	import '../../app.postcss';
	import '../../app.css';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import {
		Sidebar,
		SidebarGroup,
		SidebarItem,
		SidebarWrapper,
		Drawer,
		CloseButton,
		SidebarBrand,
		DarkMode
	} from 'flowbite-svelte';
	import { sineIn } from 'svelte/easing';
	import { Icon } from 'svelte-boxicons';
	import { NAVIGATION_ITEMS, SECONDARY_NAVIGATION_ITEMS } from '@config/navigation';
	import { accessToken } from '@config/stores';
	import { get } from 'svelte/store';

	let transitionParams = {
		x: -320
	};

	let breakPoint: number = 1024;
	let width: number;
	let backdrop: boolean = false;
	let activateClickOutside = false;
	let drawerHidden: boolean = false;
	// $: if (width >= breakPoint) {
	// 	drawerHidden = false;
	// 	activateClickOutside = false;
	// } else {
	// 	drawerHidden = true;
	// 	activateClickOutside = true;
	// }
	onMount(() => {
		if ($accessToken === undefined || $accessToken === '') {
			window.location.assign('/login');
		}

		if (width >= breakPoint) {
			drawerHidden = false;
			activateClickOutside = false;
		} else {
			drawerHidden = true;
			activateClickOutside = true;
		}
	});
	const toggleSide = () => {
		if (width < breakPoint) {
			drawerHidden = !drawerHidden;
		}
	};
	$: activeUrl = $page.url.pathname;
</script>

<svelte:window bind:innerWidth={width} />

<div class="pageWrapper">
	<Drawer
		transitionType="in:fly"
		{backdrop}
		{transitionParams}
		bind:hidden={drawerHidden}
		bind:activateClickOutside
		class="pb-32 h-screen sticky top-0"
		id="sidebar"
	>
		<div class="flex items-center">
			<CloseButton on:click={() => (drawerHidden = true)} class="mb-4 dark:text-white lg:hidden" />
		</div>
		<Sidebar>
			<SidebarWrapper divClass="overflow-y-auto py-4 px-3 rounded dark:bg-gray-800">
				<SidebarBrand
					site={{
						name: 'Quiz-App',
						href: '/',
						img: '/images/image-2@2x.jpg'
					}}
				/>
				<SidebarGroup>
					{#each NAVIGATION_ITEMS as navigationItem}
						<SidebarItem
							label={navigationItem.label}
							href={navigationItem.href}
							on:click={toggleSide}
							active={activeUrl === navigationItem.href}
						>
							<svelte:fragment slot="icon">
								<Icon name={navigationItem.icon} />
							</svelte:fragment>
						</SidebarItem>
					{/each}
				</SidebarGroup>
				<SidebarGroup border>
					{#each SECONDARY_NAVIGATION_ITEMS as navigationItem}
						<SidebarItem
							label={navigationItem.label}
							href={navigationItem.href}
							on:click={toggleSide}
							active={activeUrl === navigationItem.href}
						>
							<svelte:fragment slot="icon">
								<Icon name={navigationItem.icon} />
							</svelte:fragment>
						</SidebarItem>
					{/each}
				</SidebarGroup>
				<DarkMode class="dark:hover:text-white hover:text-gray-900 mt-2" />
			</SidebarWrapper>
		</Sidebar>
	</Drawer>
	<div class="flex px-4 w-full mt-8">
		<main class="w-full lg:ml-64mx-auto">
			<slot />
		</main>
	</div>
</div>
