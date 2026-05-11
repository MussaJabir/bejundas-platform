from django_hosts import host, patterns

host_patterns = patterns(
    "",
    host(r"financial", "apps.leads.urls", name="financial"),
    host(r"construction", "apps.leads.urls", name="construction"),
    host(r"energies", "apps.leads.urls", name="energies"),
    host(r"farming", "apps.leads.urls", name="farming"),
    host(r"investments", "apps.leads.urls", name="investments"),
    host(r"technologies", "apps.core.urls_redirect", name="technologies"),
    host(r"www", "config.urls", name="www"),
    host(r"", "config.urls", name="hub"),
)
