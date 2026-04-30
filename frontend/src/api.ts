import type { ApiError, DisplayControlResponse, DisplayListResponse } from "./types";

const API_BASE = "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
	const response = await fetch(`${API_BASE}${path}`, {
		...init,
		headers: {
			"Content-Type": "application/json",
			...(init?.headers ?? {}),
		},
	});

	if (!response.ok) {
		const fallback: ApiError = {
			code: "request_failed",
			message: `Request failed with status ${response.status}`,
		};

		try {
			const json = await response.json();
			if (json?.detail?.code && json?.detail?.message) {
				const detailError = json.detail as ApiError;
				throw detailError;
			}
			if (json?.code && json?.message) {
				const directError = json as ApiError;
				throw directError;
			}
		} catch (error) {
			if (error && typeof error === "object" && "code" in error && "message" in error) {
				throw error as ApiError;
			}
			throw fallback;
		}

		throw fallback;
	}

	return (await response.json()) as T;
}

export async function fetchDisplays(): Promise<DisplayListResponse> {
	return request<DisplayListResponse>("/displays");
}

export async function switchDisplay(displayId: string): Promise<DisplayControlResponse> {
	return request<DisplayControlResponse>(`/displays/${displayId}/switch`, {
		method: "POST",
		body: JSON.stringify({ params: {} }),
	});
}

export async function stopDisplay(displayId: string): Promise<DisplayControlResponse> {
	return request<DisplayControlResponse>(`/displays/${displayId}/stop`, {
		method: "POST",
	});
}
