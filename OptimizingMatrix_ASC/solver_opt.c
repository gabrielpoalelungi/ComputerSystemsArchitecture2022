/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"

/*
 * Add your optimized implementation here
 */
double* my_solver(int N, double *A, double* B) {
	register int i = 0;
	register int j = 0;
	register int k = 0;
	// int bi = 0;
	// int bj = 0;
	// int bk = 0;
	// int blockSize = 50;
	double *BA = malloc(N * N * sizeof(double));
	
	// BA = B X A, where A is upper triangular matrix
	for (i = 0; i < N; i++) {
		double *orig_B = &B[i*N];
		for (j = 0; j < N; j++) {
			register double sum = 0.0;
			double *pB = orig_B;
			double *pA = &A[j];
			// Here, k < N is replaced with k <= j because A is upper triangular matrix
			for (k = 0; k <= j; k++) {
				sum += *pB * *pA;
				pB++;
				pA += N;
			}
			BA[i * N + j] = sum;
		}
	}
	
	double *BAAt = malloc (N * N * sizeof(double));

	//BAAt = BA x At
	for (i = 0; i < N; i++) {
		double *orig_BA = &BA[i * N];
	 	for (j = 0; j < N; j++) {
			double *pBA = orig_BA + j;
	 		register double sum = 0.0;
	 		// Here, k = 0 is replaced with k = j, because At is lower triangular matrix
	 		for (k = j; k < N; k++) {
	 			// for transpose, instead of A[k * N + j], we have A[j * N + k]
	 			sum += *pBA * A[j * N + k];
				pBA++;
			}
	 		BAAt[i * N + j] = sum;
	 	}
	}
	
	// BtB = Bt * B
	double *BtB = malloc (N * N * sizeof(double));
	 for (i = 0; i < N; i++)
	 	for (k = 0; k < N; k++) {

	 		for (j = 0; j < N; j++)
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
