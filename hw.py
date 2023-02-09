def quadratic_ex(a, b, c):
    D = b ** 2 - 4 * a * c
    if D < 0:
        return None
    if D == 0:
        return -b / (2 * a)
    return (-b + D ** 0.5) / (2 * a), (-b - D ** 0.5) / (2 * a)


if __name__ == "__main__":
    print(quadratic_ex(1, 5, 4))
