import app from './hono/webs';
import { email } from './email/email';
import userService from './service/user-service';
import verifyRecordService from './service/verify-record-service';
import emailService from './service/email-service';
import kvObjService from './service/kv-obj-service';
import oauthService from "./service/oauth-service";
import analysisService from './service/analysis-service';

async function healthResponse(env) {
	const checks = {
		d1: false,
		kv: false,
		assets: Boolean(env.assets),
	};

	try {
		const row = await env.db.prepare('SELECT 1 AS ok').first();
		checks.d1 = Number(row?.ok) === 1;
	} catch (error) {
		checks.d1 = false;
	}

	try {
		await env.kv.get('__zerolocal_health__');
		checks.kv = true;
	} catch (error) {
		checks.kv = false;
	}

	const ok = Object.values(checks).every(Boolean);
	return new Response(JSON.stringify({
		status: ok ? 'ok' : 'degraded',
		service: 'cloud-mail',
		revision: env.zerolocal_revision || 'unknown',
		checks,
	}), {
		status: ok ? 200 : 503,
		headers: {
			'content-type': 'application/json; charset=utf-8',
			'cache-control': 'no-store',
		},
	});
}

export default {
	async fetch(req, env, ctx) {

		const url = new URL(req.url)

		if (url.pathname === '/health' || url.pathname === '/api/health') {
			return healthResponse(env);
		}

		if (url.pathname.startsWith('/api/')) {
			url.pathname = url.pathname.replace('/api', '')
			req = new Request(url.toString(), req)
			return app.fetch(req, env, ctx);
		}

		if (['/static/','/attachments/'].some(p => url.pathname.startsWith(p))) {
			return await kvObjService.toObjResp( { env }, url.pathname.substring(1));
		}

		return env.assets.fetch(req);
	},
	email: email,
	async scheduled(c, env, ctx) {
		if (c.cron === '*/30 * * * *') {
			await analysisService.refreshEchartsCache({ env })
			return;
		}

		await verifyRecordService.clearRecord({ env })
		await userService.resetDaySendCount({ env })
		await emailService.completeReceiveAll({ env })
		await oauthService.clearNoBindOathUser({ env })
		await analysisService.refreshEchartsCache({ env })
	},
};
