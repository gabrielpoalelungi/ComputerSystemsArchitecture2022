/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"

/*
 * Add your unoptimized implementation here
 */
double* my_solver(int N, double *A, double* B) {
	int i, j, k;
	double *BA = malloc(N * N * sizeof(double));
	
	//BA = B X A, where A is upper triangular matrix
	for (i = 0; i < N; i++)
		for (j = 0; j < N; j++) {
			BA[i * N + j] = 0;
			// Here, k < N is replaced with k <= j because A is upper triangular matrix
			for (k = 0; k <= j; k++)
				BA[i * N + j] += B[i * N + k] * A[k * N + j];
		}

	double *BAAt = malloc (N * N * sizeof(double));

	//BAAt = BA x At
	for (i = 0; i < N; i++)
		for (j = 0; j < N; j++) {
			BAAt[i * N + j] = 0;
			// Here, k = 0 is replaced with k = j, because At is lower triangular matrix
			for (k = j; k < N; k++)
				// for transpose, instead of A[k * N + j], we have A[j * N + k]
				BAAt[i * N + j] += BA[i * N + k] * A[j * N + k];
		}
	
	// BtB = Bt * B
	double *BtB = malloc (N * N * sizeof(double));
	for (i = 0; i < N; i++)
		for (j = 0; j < N; j++) {
			BtB[i * N + j] = 0;

			for (k = 0; k < N; k++)
				BtB[i * N + j] += B[k * N + i] * B[k * N + j];
		}

	double *result = malloc (N * N * sizeof(double));
	for (i = 0; i < N; i++)
		for (j = 0; j < N; j++)
			result[i * N + j] = BAAt[i * N + j] + BtB[i * N + j];

	free(BA);
	free(BAAt);
	free(BtB);
	return result;
}

