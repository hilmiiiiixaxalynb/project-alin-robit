def smart_num(x):
    """Kembalikan int jika nilainya bulat, float jika tidak."""
    rounded = round(x, 9)  # buang floating point noise dulu
    return int(rounded) if rounded == int(rounded) else round(rounded, 6)


def tambah_matrix(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Ukuran matrix harus sama untuk penjumlahan.")
    return [[smart_num(A[i][j] + B[i][j]) for j in range(len(A[0]))] for i in range(len(A))]


def kurang_matrix(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Ukuran matrix harus sama untuk pengurangan.")
    return [[smart_num(A[i][j] - B[i][j]) for j in range(len(A[0]))] for i in range(len(A))]


def kali_matrix(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Kolom matrix A harus sama dengan baris matrix B untuk perkalian.")
    return [
        [smart_num(sum(A[i][k] * B[k][j] for k in range(len(B)))) for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def transpose_matrix(A):
    return [[smart_num(A[i][j]) for i in range(len(A))] for j in range(len(A[0]))]


def determinan_matrix(A):
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("Determinan hanya bisa dihitung untuk matrix persegi.")
    if n == 1:
        return smart_num(A[0][0])
    if n == 2:
        return smart_num(A[0][0] * A[1][1] - A[0][1] * A[1][0])
    det = 0
    for c in range(n):
        minor = [[A[r][col] for col in range(n) if col != c] for r in range(1, n)]
        det += ((-1) ** c) * A[0][c] * determinan_matrix(minor)
    return smart_num(det)


def invers_matrix(A):
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("Invers hanya bisa dihitung untuk matrix persegi.")
    det = determinan_matrix(A)
    if det == 0:
        raise ValueError("Matrix singular (determinan = 0), tidak memiliki invers.")

    # Augmented matrix [A | I]
    M = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(A)]

    for col in range(n):
        # Pivot
        pivot = None
        for row in range(col, n):
            if M[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            raise ValueError("Matrix singular, tidak bisa diinvers.")
        M[col], M[pivot] = M[pivot], M[col]
        factor = M[col][col]
        M[col] = [x / factor for x in M[col]]
        for row in range(n):
            if row != col:
                factor = M[row][col]
                M[row] = [M[row][k] - factor * M[col][k] for k in range(2 * n)]

    result = [[smart_num(M[i][n + j]) for j in range(n)] for i in range(n)]
    return result