# Kata URL: https://www.codewars.com/kata/51646de80fd67f442c000013

def strip_url_params(url, params_to_strip = []):
    params  = []
    seen = []
    if "?" in url:
        queries = url[url.index("?")+1:].split("&")
        for i in range(0,len(queries)):
            if queries[i][0] not in seen and queries[i][0] not in params_to_strip:
                seen.append(queries[i][0])
                params.append(queries[i])
        return(url[:url.index("?")+1]+"&".join(params))
    else:
        return url
