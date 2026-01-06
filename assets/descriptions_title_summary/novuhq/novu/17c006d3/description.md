# Remove `ApiException` in favor of `BadRequestException`

Replace custom `ApiException` with standard NestJS `BadRequestException` across all services (`api`, `worker`, `ws`, `webhook`, `application-generic`).