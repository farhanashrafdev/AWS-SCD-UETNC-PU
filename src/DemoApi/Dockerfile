# Reference-only: not built or pushed anywhere as part of this demo. It
# exists so gitops/manifests/demo-api/deployment.yaml references a
# plausible, buildable image instead of an imaginary one.

FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src
COPY src/DemoApi/DemoApi.csproj src/DemoApi/
RUN dotnet restore src/DemoApi/DemoApi.csproj
COPY src/DemoApi/ src/DemoApi/
RUN dotnet publish src/DemoApi/DemoApi.csproj -c Release -o /app --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS final
WORKDIR /app
COPY --from=build /app .
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080
ENTRYPOINT ["dotnet", "DemoApi.dll"]
