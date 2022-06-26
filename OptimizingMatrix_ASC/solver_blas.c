/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"
#include <cblas.h>
#include <string.h>

/* 
 * Add your BLAS implementation here
 */
double* my_solver(int N, double *A, double *B) {
	// Used calloc instead of malloc because valgrind kept yelling
	// 'Syscall param msync(start) points to uninitialised byte(s)'
	double *BA = calloc(N * N, sizeof(double));
	memcpy(BA, B, N*N * sizeof(double));

	// BA = B * A
	// Final result in BA;
	// CblasRight => BA = BA x A, not BA = A x BA
	cblas_dtrmm(CblasRowMajor, CblasRight,
				CblasUpper, CblasNoTrans,
				CblasNonUnit, N, N,
				1.0, A, N,
				BA, N
				);

	double *BAAt = calloc(N*N, sizeof(double));
	cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasTrans,
				N, N, N, 1.0, BA, N, A, N, 1.0,
				BAAt, N
				);
	
	double *BtB = calloc(N * N, sizeof(double));
	cblas_dgemm(CblasRowMajor, CblasTrans, CblasNoTrans,
				N, N, N, 1.0, B, N, B, N, 1.0,
				BtB, N
				);

	double *result = calloc (N * N, sizeof(double));
	for (int i = 0; i < N; i++)
		for (int j = 0; j < N; j++)
			result[i * N + j] = BAAt[i * N + j] + BtB[i * N + j];

	free(BA);
	free(BAAt);
	free(BtB);
	return result;
}
